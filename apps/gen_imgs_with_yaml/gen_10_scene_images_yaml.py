import os
import argparse
import yaml
import re
from litellm import completion
from dotenv import load_dotenv

load_dotenv()

def parse_yaml_from_text(text):
    # Try to extract content between ```yaml and ```
    match = re.search(r'```yaml\s*(.*?)\s*```', text, re.DOTALL)
    if match:
        return match.group(1)
    
    # If no ```yaml block, maybe just ``` 
    match = re.search(r'```\s*(.*?)\s*```', text, re.DOTALL)
    if match:
        return match.group(1)
        
    return text

def main():
    parser = argparse.ArgumentParser(description='Generate 10 scene images YAML config based on context.')
    parser.add_argument('--context', type=str, required=True, help='The context/story for the 10 images')
    parser.add_argument('--model', type=str, default=os.environ.get('MODEL', 'gemini/gemini-2.5-pro'), help='The LLM model to use')
    parser.add_argument('--base_url', type=str, default=os.environ.get("LITELLM_BASE_URL", None), help='Base URL for the litellm provider')
    parser.add_argument('--output', type=str, default='outputs/scene_10_images.yaml', help='Output YAML file path')
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    config_path = '/home/dd/work/diep/openhands/apps/mcp_gen_img_vid_with_refs/ref/pics_config.yaml'
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            ref_config = yaml.safe_load(f)
    except Exception as e:
        print(f"Error reading config file {config_path}: {e}")
        return

    prompt = f"""You are an expert AI image prompt engineer and director.
I will give you a context/story, and you need to design a sequence of exactly 10 images that tell this story.

Context: "{args.context}"

Available References (from pics_config.yaml):
{yaml.dump(ref_config, allow_unicode=True)}

IMPORTANT REQUIREMENTS:
1. You must maintain STRICT consistency across all 10 images for the character's clothing, accessories, and overall appearance. For example, if you choose a specific dress or item for the character in the first image, they MUST wear/use that exact same reference in all 10 images to ensure continuity.
2. You do not have to use every reference category. You can leave background_reference_path, pose_reference_path, or item_reference_paths blank/null if you want the AI to freely generate those aspects.
3. Khi sinh ra chuỗi `prompt` cho mỗi bức ảnh, LLM **PHẢI** mô tả rõ ràng sự tương ứng (mapping) giữa nhân vật/vật thể trong prompt với thứ tự của các reference được truyền vào. Ví dụ: "Người đàn ông (khớp với Face Reference 2) đang kéo ghế cho người phụ nữ (khớp với Face Reference 1). Người phụ nữ đang mặc một chiếc váy (khớp với Item Reference 1) và đi đôi giày (khớp với Item Reference 2)..." Điều này rất quan trọng để mô hình sinh ảnh (như Gemini) hiểu được tham chiếu nào ứng với chủ thể nào trong bối cảnh.
4. Your output must be ONLY a valid YAML array of 10 objects. Do not include any explanation.
5. Each object in the YAML array must match the parameters of the `generate_custom_scene_image` tool exactly:
   - prompt (string): Detailed description of the scene, character action, and environment.
   - face_reference_paths (list of strings): Paths to face references.
   - background_reference_path (string or null): Path to background reference.
   - pose_reference_path (string or null): Path to pose reference.
   - item_reference_paths (list of strings or null): Paths to item/clothing/accessory references.

Example output format:
```yaml
- prompt: "Character walking in the park..."
  face_reference_paths: ["ref/face/havy.jpg"]
  background_reference_path: null
  pose_reference_path: "ref/pose/walking.jpg"
  item_reference_paths: ["ref/item/white_dress.jpg"]
- prompt: "Character sitting on a bench..."
  ...
```

Generate the YAML for the 10 images now:
"""

    print(f"Calling LLM ({args.model}) to generate YAML...")
    try:
        kwargs = {}
        if args.base_url:
            kwargs['base_url'] = args.base_url
        
        api_key = os.environ.get("GOOGLE_API_KEY")
        if api_key:
            kwargs['api_key'] = api_key
            
        response = completion(
            model=args.model,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        
        content = response.choices[0].message.content
        yaml_content = parse_yaml_from_text(content)
        
        # Validate YAML
        yaml.safe_load(yaml_content)
        
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(yaml_content)
            
        print(f"Successfully generated and saved YAML to {args.output}")
        
    except Exception as e:
        error_msg = str(e).lower()
        if "provider" in error_msg or "badrequesterror" in error_msg or "litellm" in error_msg:
            print(f"Lỗi: Bạn cần cung cấp tên provider cho model. Ví dụ thay vì '{args.model}', hãy thử 'openai/{args.model}' nếu bạn dùng proxy.")
        print(f"Error generating or saving YAML: {e}")

if __name__ == "__main__":
    main()

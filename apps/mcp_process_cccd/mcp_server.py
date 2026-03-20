import os
import json
import asyncio
import logging
from mcp.server.fastmcp import FastMCP
from playwright.async_api import async_playwright
import google.generativeai as genai
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=os.sys.stderr  # Đảm bảo log ra stderr để không xung đột với JSONRPC
)
logger = logging.getLogger(__name__)

load_dotenv()

# Initialize FastMCP
mcp = FastMCP("CCCD_Processor")

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@mcp.tool()
async def extract_cccd_with_gemini(photo_1_path: str, photo_2_path: str) -> str:
    """
    Extract information from 2 CCCD images (front and back) using Gemini.
    Returns a JSON string with the extracted data.
    """
    if not os.path.exists(photo_1_path) or not os.path.exists(photo_2_path):
        return json.dumps({
            "fullname": "không xác định",
            "id_number": "không xác định",
            "dob": "1111-11-11",
            "address": "không xác định",
            "issue_date": "1111-11-11",
            "issue_place": "không xác định",
            "status": "ERROR",
            "message": "File không tồn tại"
        })

    logger.info("Đang phân tích ảnh...")
    
    try:
        # Upload files to Gemini
        front_file = await asyncio.to_thread(genai.upload_file, photo_1_path)
        back_file = await asyncio.to_thread(genai.upload_file, photo_2_path)
        
        model_name = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")
        model = genai.GenerativeModel(model_name)
        
        prompt = """Bạn là chuyên gia OCR dữ liệu hành chính Việt Nam. Trích xuất thông tin từ 2 ảnh CCCD thành JSON.
Quy tắc:
- `dob`, `issue_date`: Định dạng `YYYY-MM-DD`.
- `id_number`: Chuỗi 12 số.
- Nếu mờ/thiếu: Dùng giá trị mặc định `1111-11-11` (date) và `không xác định` (text). Đặt `status` là `WARNING`.
- Nếu đầy đủ: Đặt `status` là `OK`.
- JSON Output duy nhất: {"fullname": "...", "id_number": "...", "dob": "...", "address": "...", "issue_date": "...", "issue_place": "...", "status": "..."}."""

        response = await asyncio.to_thread(model.generate_content, [prompt, front_file, back_file])
        
        # Clean up files
        await asyncio.to_thread(genai.delete_file, front_file.name)
        await asyncio.to_thread(genai.delete_file, back_file.name)
        
        # Extract JSON from response
        text = response.text
        # Find JSON block if wrapped in markdown
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
            
        return text
    except Exception as e:
        logger.error(f"Lỗi khi phân tích ảnh: {e}")
        return json.dumps({
            "fullname": "không xác định",
            "id_number": "không xác định",
            "dob": "1111-11-11",
            "address": "không xác định",
            "issue_date": "1111-11-11",
            "issue_place": "không xác định",
            "status": "WARNING"
        })

@mcp.tool()
async def automate_web_submission(json_data: str, photo_1_path: str, photo_2_path: str) -> str:
    """
    Automate web submission using Playwright.
    """
    if not os.path.exists(photo_1_path) or not os.path.exists(photo_2_path):
        return "lỗi khi upload: File không tồn tại"

    data = json.loads(json_data)
    logger.info(f"Đang đăng nhập... và điền form cho CCCD {data.get('id_number')}...")
    logger.info(json_data)
    
    app_url = os.getenv("APP_URL", "http://127.0.0.1:5005")
    username = os.getenv("ADMIN_USERNAME", "admin")
    password = os.getenv("ADMIN_PASSWORD", "secret")
    
    is_headless = os.getenv("HEADLESS", "true").lower() == "true"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=is_headless)
        page = await browser.new_page()
        
        try:
            # Login
            await page.goto(f"{app_url}/login")
            await page.fill("#username", username)
            await page.fill("#password", password)
            await page.click("button[type='submit']")
            
            # Wait for navigation
            await page.wait_for_url(f"{app_url}/")
            
            # Go to upload
            await page.goto(f"{app_url}/upload")
            
            # Fill form
            await page.fill("#fullname", data.get("fullname", ""))
            await page.fill("#id_number", data.get("id_number", ""))
            await page.fill("#dob", data.get("dob", ""))
            await page.fill("#address", data.get("address", ""))
            await page.fill("#issue_date", data.get("issue_date", ""))
            await page.fill("#issue_place", data.get("issue_place", ""))
            
            # Upload files
            await page.set_input_files("#photo_1", photo_1_path)
            await page.set_input_files("#photo_2", photo_2_path)
            
            # Submit
            await page.click("button[type='submit']")
            
            # Wait for navigation or flash message
            await page.wait_for_load_state("networkidle")
            
            await browser.close()
            logger.info(f"Upload completed for {photo_1_path}")
            return "đã upload lên hệ thống"
        except Exception as e:
            await browser.close()
            logger.info(f"Lỗi khi upload: {e}")
            return f"lỗi khi upload: {e}"

@mcp.tool()
async def process_and_submit_cccd(photo_1_path: str, photo_2_path: str) -> str:
    """
    Master tool to process CCCD images and submit them to the web app.
    """
    if not os.path.exists(photo_1_path) or not os.path.exists(photo_2_path):
        return "Lỗi: File không tồn tại."

    # Step 1: Extract data
    json_data = await extract_cccd_with_gemini(photo_1_path, photo_2_path)
    
    try:
        data = json.loads(json_data)
        status = data.get("status", "UNKNOWN")
    except:
        status = "ERROR"
        
    if status == "ERROR":
        return "Lỗi nghiêm trọng khi trích xuất thông tin, dừng quá trình submit."

    # Step 2: Submit data
    submit_result = await automate_web_submission(json_data, photo_1_path, photo_2_path)
    
    return f"Đã trích xuất thành công với trạng thái {status} và {submit_result}"

if __name__ == "__main__":
    mcp.run()

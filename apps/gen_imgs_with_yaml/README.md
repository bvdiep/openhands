# gen_yaml_10_pics

Pipeline tạo 10 ảnh kể chuyện từ một đoạn mô tả (context/story), sử dụng Gemini image generation thông qua MCP protocol.

## Quy trình 2 bước

```
Context/Story  ──►  gen_10_scene_images_yaml.py  ──►  scene YAML  ──►  generate_from_yaml.py  ──►  10 ảnh + mapping.yaml
```

**Bước 1:** Dùng LLM chuyển đổi câu chuyện thành file YAML chứa 10 scene (mỗi scene có prompt + reference images).

**Bước 2:** Đọc file YAML, gọi MCP server (`mcp_gen_img_vid_with_refs`) qua giao thức MCP để sinh ảnh từng scene.

---

## Cài đặt

```bash
pip install -r requirements.txt
```

Yêu cầu MCP server tại `../mcp_gen_img_vid_with_refs/` đã được cấu hình (venv + Google API key).

### Cấu hình references

File `../mcp_gen_img_vid_with_refs/ref/pics_config.yaml` định nghĩa các reference images sẵn có:

```yaml
faces:
    havy:
        - /path/to/ref/hv01.png
    diep:
        - /path/to/ref/dd01.png
backgrounds:
    office:
        - /path/to/ref/vp01.jpg
items:
    dress:
        - /path/to/ref/vay_hoa_01.jpg
    bag:
        - /path/to/ref/tuixach_01.jpg
```

LLM sẽ đọc cấu hình này để chọn references phù hợp khi sinh YAML.

---

## Script 1: `gen_10_scene_images_yaml.py`

Sinh file YAML chứa 10 scene từ một đoạn mô tả (context).

### Tham số

| Tham số | Bắt buộc | Mặc định | Mô tả |
|---------|----------|----------|-------|
| `--context` | Có | - | Đoạn mô tả câu chuyện / bối cảnh |
| `--model` | Không | `gemini/gemini-2.5-pro` | LLM model (qua litellm) |
| `--base_url` | Không | `$LITELLM_BASE_URL` | Base URL cho litellm provider |
| `--output` | Không | `outputs/scene_10_images.yaml` | Đường dẫn file YAML đầu ra |

### Ví dụ

```bash
python gen_10_scene_images_yaml.py \
  --context "Havy là một marketer trẻ. Một ngày làm việc của cô bắt đầu từ phòng ngủ, đi làm, thuyết trình, nghỉ trưa, rồi về nhà." \
  --output outputs/scene_10_images_office_01.yaml
```

```bash
python gen_10_scene_images_yaml.py \
  --context "Havy và Diep có một buổi hẹn hò ăn tối lãng mạn tại nhà hàng." \
  --model gemini/gemini-2.5-pro \
  --output outputs/scene_10_images_dinner_01.yaml
```

### Format YAML đầu ra

```yaml
- prompt: "Havy (khớp với Face Reference 1) đang đứng vươn vai trong phòng ngủ..."
  face_reference_paths:
    - "/path/to/ref/hv01.png"
  background_reference_path: "/path/to/ref/bedroom_01.png"
  pose_reference_path: null
  item_reference_paths:
    - "/path/to/ref/vay_hoa_01.jpg"
    - "/path/to/ref/giay_01.png"
    - "/path/to/ref/tuixach_01.jpg"

- prompt: "Havy (khớp với Face Reference 1) đang ngồi kiểm tra email..."
  ...
```

---

## Script 2: `generate_from_yaml.py`

Đọc file YAML scene và gọi MCP server để sinh ảnh từng scene qua giao thức MCP (stdio).

> Script sử dụng Python từ venv của MCP server (`../mcp_gen_img_vid_with_refs/.venv/bin/python`).

### Tham số

| Tham số | Bắt buộc | Mặc định | Mô tả |
|---------|----------|----------|-------|
| `--input`, `-i` | Có | - | Đường dẫn file YAML đầu vào |
| `--output-dir`, `-o` | Không | Cùng thư mục với file YAML | Thư mục gốc chứa kết quả |

### Ví dụ

```bash
# Cách 1: chạy trực tiếp (shebang đã trỏ tới MCP venv)
./generate_from_yaml.py -i outputs/scene_10_images_office_01.yaml

# Cách 2: gọi rõ Python
../mcp_gen_img_vid_with_refs/.venv/bin/python generate_from_yaml.py \
  -i outputs/scene_10_images_dinner_01.yaml

# Cách 3: chỉ định thư mục output riêng
./generate_from_yaml.py \
  -i outputs/scene_10_images_office_01.yaml \
  -o /tmp/my_output
```

### Kết quả

Với file đầu vào `outputs/scene_10_images_office_01.yaml`, script tạo thư mục:

```
outputs/scene_10_images_office_01/
├── scene_01.png
├── scene_02.png
├── scene_03.png
├── ...
├── scene_10.png
└── mapping.yaml
```

File `mapping.yaml`:

```yaml
- scene: 1
  filename: scene_01.png
  prompt: "Buổi sáng bắt đầu. Một người phụ nữ trẻ tên Havy..."
- scene: 2
  filename: scene_02.png
  prompt: "Havy đang ngồi kiểm tra email..."
...
```

---

## Pipeline hoàn chỉnh

```bash
# Bước 1: Sinh YAML từ câu chuyện
python gen_10_scene_images_yaml.py \
  --context "Havy là một marketer, ngày làm việc từ sáng đến tối." \
  --output outputs/scene_10_images_office_01.yaml

# Bước 2: Sinh ảnh từ YAML (chạy tuần tự từng scene, mỗi scene spawn 1 MCP server)
./generate_from_yaml.py -i outputs/scene_10_images_office_01.yaml

# Kết quả tại: outputs/scene_10_images_office_01/
```

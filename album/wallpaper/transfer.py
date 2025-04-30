import os
from PIL import Image
import re

def process_images():
    # 支持的图片格式
    image_formats = ('.jpg', '.jpeg', '.png', '.webp', '.heic', '.svg', '.tiff', '.tif', '.bmp', '.dpx', '.exr')
    gif_format = ('.gif',)
    url = "https://randolfluo.top/album/wallpaper/img/"
    
    # 检查img子目录是否存在
    img_dir = os.path.join(os.path.dirname(__file__), 'img')
    if not os.path.exists(img_dir) or not os.path.isdir(img_dir):
        print(f"Error: Directory '{img_dir}' does not exist!")
        return
    
    # 初始化计数器
    img_counter = 1
    gif_counter = 1
    gallery_content = ["{% gallery %}"]  # 初始化画廊内容
    url_links = []  #初始化url链接
    
    # 处理img目录中的文件
    for filename in sorted(os.listdir(img_dir)):  # sorted for consistent ordering
        filepath = os.path.join(img_dir, filename)
        if not os.path.isfile(filepath):
            continue
            
        try:
            name, ext = os.path.splitext(filename)
            ext = ext.lower()
            
            # 处理GIF文件（保留原格式）
            if ext in gif_format:
                # 确保文件名唯一
                while True:
                    new_filename = f"gif_{gif_counter}.gif"
                    new_filepath = os.path.join(img_dir, new_filename)
                    if not os.path.exists(new_filepath):
                        break
                    gif_counter += 1
                
                os.rename(filepath, new_filepath)
                print(f'{filename} -> {new_filename}')
                gallery_content.append(f"![](./img/{new_filename})")
                url_links.append("- " + url + new_filename)
                gif_counter += 1
            
            # 处理其他图片文件（转为PNG）
            elif ext in image_formats:
                # 确保文件名唯一
                while True:
                    new_filename = f"img_{img_counter}.png"
                    new_filepath = os.path.join(img_dir, new_filename)
                    if not os.path.exists(new_filepath):
                        break
                    img_counter += 1
                
                with Image.open(filepath) as img:
                    # 处理透明通道
                    if img.mode in ('RGBA', 'P'):
                        img = img.convert('RGB')
                    img.save(new_filepath, 'PNG')
                
                if filepath != new_filepath:  # 避免删除新文件
                    os.remove(filepath)
                print(f'{filename} -> {new_filename}')
                gallery_content.append(f"![](./img/{new_filename})")
                url_links.append("- " + url + new_filename)
                img_counter += 1
                
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
            continue
    
    # 结束画廊标记
    gallery_content.append("{% endgallery %}")
    
    # 读取并更新index.txt
    index_file = os.path.join(os.path.dirname(__file__), 'index.md')
    try:
        # 读取现有内容
        if os.path.exists(index_file):
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            # 删除旧的画廊内容
            pattern = re.compile(r'{%\s*gallery\s*%}.*?{%\s*endgallery\s*%}', re.DOTALL)
            cleaned_content = re.sub(pattern, '', content)
        else:
            cleaned_content = ''
        
        # 写入新内容
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_content.strip() + '\n\n' + '\n'.join(gallery_content))
            
    except Exception as e:
        print(f"Error writing to {index_file}: {str(e)}")
    
    url_path = os.path.join(os.path.dirname(__file__), 'url.txt')
    
    try:
        with open(url_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(url_links))
        print("URL links have been saved to url.txt")
    except Exception as e:
        print(f"Error writing to url.txt: {str(e)}")
    

if __name__ == "__main__":
    process_images()
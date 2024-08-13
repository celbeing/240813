import streamlit as st
import pytesseract
from PIL import Image
import os

# Tesseract 실행 파일 경로 설정 (Windows 사용자의 경우 필요할 수 있음)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 캐시 디렉토리 생성
if not os.path.exists(".cache"):
    os.mkdir(".cache")

# 파일 업로드 전용 폴더
if not os.path.exists(".cache/files"):
    os.mkdir(".cache/files")

st.title("이미지에서 텍스트 추출")

# 처음 1번만 실행하기 위한 코드
if "messages" not in st.session_state:
    # 대화기록을 저장하기 위한 용도로 생성한다.
    st.session_state["messages"] = []

# 탭을 생성
main_tab1, main_tab2 = st.tabs(["이미지", "대화내용"])

# 사이드바 생성
with st.sidebar:
    # 초기화 버튼 생성
    clear_btn = st.button("대화 초기화")

    # 이미지 업로드
    uploaded_file = st.file_uploader("이미지 업로드", type=["jpg", "jpeg", "png"])

# 이전 대화를 출력
def print_messages():
    for chat_message in st.session_state["messages"]:
        main_tab2.chat_message(chat_message["role"]).write(chat_message["content"])

# 새로운 메시지를 추가
def add_message(role, message):
    st.session_state["messages"].append({"role": role, "content": message})

# 이미지 파일을 캐시 저장
@st.cache_resource(show_spinner="업로드한 이미지를 처리 중입니다...")
def process_imagefile(file):
    # 업로드한 파일을 캐시 디렉토리에 저장합니다.
    file_content = file.read()
    file_path = f"./.cache/files/{file.name}"

    with open(file_path, "wb") as f:
        f.write(file_content)

    return file_path

# 이미지에서 텍스트 추출
def extract_text_from_image(image_filepath):
    # 이미지 열기
    image = Image.open(image_filepath)
    # 이미지에서 텍스트 추출
    text = pytesseract.image_to_string(image)
    return text

# 초기화 버튼이 눌리면...
if clear_btn:
    st.session_state["messages"] = []

# 이전 대화 기록 출력
print_messages()

# 이미지가 업로드 되었다면...
if uploaded_file:
    # 이미지 파일을 처리
    image_filepath = process_imagefile(uploaded_file)
    main_tab1.image(image_filepath)

    # 텍스트 추출
    extracted_text = extract_text_from_image(image_filepath)

    # 추출된 텍스트 출력
    main_tab1.write("추출된 텍스트:")
    main_tab1.text(extracted_text)

    # 대화기록에 추가
    add_message("user", "이미지에서 텍스트 추출 요청")
    add_message("assistant", extracted_text)

# 이전 대화 기록 다시 출력
print_messages()

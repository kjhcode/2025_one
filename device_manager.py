# 필요한 라이브러리 불러오기
import streamlit as st # 웹 앱을 만들 때 사용하는 라이브러리
import pandas as pd # 데이터를 표 형태로 다룰 때 사용하는 라이브러리 (엑셀처럼!)
from datetime import datetime # 현재 시간을 가져올 때 사용
import os # 파일이 있는지 확인할 때 사용

# --- 🐼 설정: 데이터 파일 이름 ---
# 여기에 기록들을 저장할 파일 이름을 정해줄 거야!
DATA_FILE = 'smart_device_log.csv'

# --- 📚 함수: 데이터 로드 및 저장 ---
# 엑셀 파일처럼 데이터를 불러오고 저장하는 함수야!
def load_data():
    # 만약 기록 파일이 있으면 불러오고, 없으면 빈 데이터프레임을 만들 거야
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    # 처음 실행할 때는 이런 열(컬럼) 이름으로 빈 표를 만들어줘
    return pd.DataFrame(columns=['학생ID', '구분', '시간'])

def save_data(df):
    # 데이터를 CSV 파일로 저장하는 함수야. index=False는 불필요한 번호가 안 생기게 하는 거야!
    df.to_csv(DATA_FILE, index=False)

# --- ✨ Streamlit 앱의 시작! ---
# 웹페이지의 제목과 아이콘, 레이아웃을 설정해줘!
st.set_page_config(
    page_title="스마트 기기 반출입 관리 앱 🐼", # 브라우저 탭에 뜨는 제목
    page_icon="📱", # 브라우저 탭에 뜨는 아이콘 (이모티콘도 돼!)
    layout="centered" # 앱 내용을 가운데로 정렬해줘
)

st.title("📱 스마트 기기 반출입 관리 앱 🐼")
st.write("우리 학생들의 스마트 기기 반출입 기록을 똑똑하게 관리해보세요! 👍")

# --- 📊 데이터 로드 (앱 시작 시 기존 기록 불러오기) ---
df = load_data()

# --- 🚀 기기 반출/반입 입력 섹션 ---
st.header("✨ 새로운 기록 추가하기")

# 'with st.form():'은 여러 입력 위젯을 하나로 묶어서 '기록하기' 버튼을 눌렀을 때만 작동하게 해줘!
with st.form("device_log_form"):
    # 학생 이름을 입력받는 칸이야
    student_id = st.text_input("👩‍🎓 학생 ID (또는 이름)", placeholder="예: 김판다 또는 10101")
    
    # '반출' 또는 '반입'을 선택하는 라디오 버튼이야
    action_type = st.radio("📚 구분", ["반출", "반입"])
    
    # 이 버튼을 눌러야 위의 입력 내용이 처리돼!
    submitted = st.form_submit_button("✅ 기록하기")

    # 버튼이 눌렸을 때 실행될 내용
    if submitted:
        if student_id: # 학생 ID가 입력되었는지 확인
            # 새로운 기록을 데이터프레임(표)에 추가할 준비를 해!
            new_entry = pd.DataFrame([{
                '학생ID': student_id,
                '구분': action_type,
                '시간': datetime.now().strftime('%Y-%m-%d %H:%M:%S') # 현재 시간을 '년-월-일 시:분:초' 형식으로 저장
            }])
            # 기존 데이터프레임과 새 기록을 합쳐줘
            df = pd.concat([df, new_entry], ignore_index=True)
            # 변경된 데이터를 다시 파일에 저장! (그래야 앱을 껐다 켜도 기록이 남아있어)
            save_data(df)
            st.success(f"**{student_id}** 학생의 기기 **{action_type}** 기록 완료! 🎉")
            # 입력 후 새로고침해서 입력창을 비워주려면 아래 코드 (선택사항, 위에 입력창이 바로 비워지지는 않지만 작동은 됨)
            # st.experimental_rerun()
        else:
            st.warning("학생 ID를 입력해주세요! 🚨")

# --- 📋 전체 반출입 기록 섹션 ---
st.header("📋 전체 반출입 기록")
if not df.empty: # 데이터프레임에 내용이 있으면 보여줘
    # 최신 기록이 맨 위로 오도록 시간 역순으로 정렬해서 보여줄게!
    st.dataframe(df.sort_values(by='시간', ascending=False).reset_index(drop=True))
else:
    st.info("아직 기록된 내용이 없어요! 첫 기록을 추가해보세요. 🐾")

# --- 📊 학생별 누적 횟수 섹션 ---
st.header("📊 학생별 누적 반출입 횟수")

if not df.empty:
    # 학생 ID별로 '반출' 횟수를 세고
    checkout_counts = df[df['구분'] == '반출']['학생ID'].value_counts().rename('반출 횟수')
    # 학생 ID별로 '반입' 횟수를 세서
    checkin_counts = df[df['구분'] == '반입']['학생ID'].value_counts().rename('반입 횟수')

    # 두 결과를 합쳐서 하나의 표로 만들어줘! (없으면 0으로 채워줘)
    cumulative_df = pd.DataFrame({
        '반출 횟수': checkout_counts,
        '반입 횟수': checkin_counts
    }).fillna(0).astype(int) # 없는 값(NaN)은 0으로 채우고 정수형으로 변환

    st.dataframe(cumulative_df)
else:
    st.info("누적 횟수를 표시할 기록이 없어요. 😊 기록을 추가해봐! ")

st.markdown("---")
st.caption("✨ 팬더랑 같이 만들어요! 멋진 앱 탄생 🥳")

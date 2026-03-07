import streamlit as st
import requests

st.set_page_config(page_title="P'Ken Exam Generator", layout="wide")

st.title("💡 เครื่องมือสร้างข้อสอบ Conversation โดย พี่เค็น")

# ส่วนบน: ใส่บทสนทนา
context = st.text_area("1. วางบทสนทนาต้นฉบับที่นี่", height=250, placeholder="ใส่ Conversation ที่ต้องการนำมาทำข้อสอบ...")

st.divider()

# ส่วนล่าง: 5 Fields สำหรับ Keywords และ Dropdown
st.subheader("2. เลือกคำที่จะเจาะช่องว่าง (Fill in the blank)")

inputs = []
cols = st.columns(5) 

for i in range(5):
    with cols[i]:
        st.markdown(f"**คำถามข้อที่ {i+1}**")
        word = st.text_input(f"คำที่เลือก", key=f"w_{i}", placeholder="เช่น although")
        category = st.selectbox(f"วัดเรื่อง", ["Tense", "Vocabulary", "Idiom", "Manner", "Logic"], key=f"c_{i}")
        inputs.append({"word": word, "type": category})

st.divider()

# ปุ่ม Generate
if st.button("🚀 Generate ข้อสอบ", type="primary", use_container_width=True):
    if not context or not any(item['word'] for item in inputs):
        st.warning("กรุณาใส่บทสนทนาและเลือกคำอย่างน้อย 1 คำครับพี่เค็น")
    else:
        WEBHOOK_URL = "https://my-n8n-production-67b5.up.railway.app/webhook/create-exam" 
        
        payload = {
            "context": context,
            "inputs": inputs
        }
        
        with st.status("🤖 AI กำลังสร้างข้อสอบให้พี่เค็นอยู่นะครับ...", expanded=True) as status:
            try:
                response = requests.post(WEBHOOK_URL, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    
                    # --- ส่วนการดึงข้อมูลและทำความสะอาด (ดึงแค่เนื้อหาข้อสอบ) ---
                    if isinstance(data, dict):
                        # หยิบค่าแรกที่เจอ (ซึ่งควรเป็นเนื้อหาข้อสอบ)
                        exam_content = list(data.values())[0]
                    else:
                        exam_content = data
                    
                    status.update(label="✅ สร้างข้อสอบสำเร็จแล้วครับ!", state="complete", expanded=False)
                    
                    st.divider()
                    st.subheader("📝 ผลลัพธ์ข้อสอบ (พี่เค็นก๊อบไปใช้ได้เลย)")
                    
                    # แสดงผลแบบ Markdown จะช่วยให้เว้นบรรทัดและทำตัวหนาสวยงาม
                    st.markdown(exam_content)
                    
                    st.balloons() # ยิงพลุฉลองความสำเร็จ!
                    
                else:
                    st.error(f"Error: n8n ตอบกลับด้วยรหัส {response.status_code}")
            except Exception as e:
                st.error(f"เชื่อมต่อ n8n ไม่ได้: {e}")

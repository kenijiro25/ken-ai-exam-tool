import streamlit as st
import requests

# ตั้งค่าหน้าจอ
st.set_page_config(page_title="P'Ken Exam Generator", layout="wide")
st.title("💡 เครื่องมือสร้างข้อสอบ Conversation โดย พี่เค็น")

# 1. ส่วนรับบทสนทนา
context = st.text_area("1. วางบทสนทนาต้นฉบับที่นี่", height=250, placeholder="ใส่ Conversation ที่ต้องการนำมาทำข้อสอบ...")

st.divider()

# 2. ส่วนเลือกคำศัพท์ 5 ข้อ
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

# 3. ปุ่มกดสร้างข้อสอบ
if st.button("🚀 Generate ข้อสอบ", type="primary", use_container_width=True):
    if not context or not any(item['word'] for item in inputs):
        st.warning("กรุณาใส่ข้อมูลให้ครบก่อนครับพี่เค็น")
    else:
        WEBHOOK_URL = "https://my-n8n-production-67b5.up.railway.app/webhook/create-exam" 
        payload = {"context": context, "inputs": inputs}
        
        with st.status("🤖 กำลังแกะห่อข้อสอบให้พี่เค็นครับ...", expanded=True) as status:
            try:
                # ส่งข้อมูลไป n8n
                response = requests.post(WEBHOOK_URL, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # --- สูตร "หยิบทุกอย่างที่ขวางหน้า" (แก้ปัญหา n8n ส่งมาไม่ตรงชื่อ) ---
                    if isinstance(data, dict) and data:
                        # ถ้าส่งมาเป็นกล่อง ให้หยิบเนื้อหาแรกที่เจอมาโชว์เลย (ไม่สนชื่อ exam_text)
                        exam_content = list(data.values())[0]
                    else:
                        # ถ้าส่งมาเป็นข้อความเพียว ๆ ก็แสดงผลทันที
                        exam_content = data
                    
                    status.update(label="✅ ดึงข้อมูลสำเร็จ!", state="complete", expanded=False)
                    st.success("✅ ได้ข้อสอบแล้วครับพี่เค็น!")
                    st.divider()
                    st.subheader("📝 ผลลัพธ์ข้อสอบ (ก๊อบไปใช้ได้เลย)")
                    st.markdown(exam_content) # แสดงผลสวยงามตาม Markdown
                    st.balloons() # ยิงพลุฉลองที่ทำสำเร็จครับพี่!
                    
                else:
                    st.error(f"Error: n8n ตอบกลับด้วยรหัส {response.status_code}")
            except Exception as e:
                # ถ้า n8n ส่งมาเละจนอ่านไม่ได้ ให้ลองโชว์แบบข้อความดิบ
                st.error(f"เกิดข้อผิดพลาด: {e}")
                if 'response' in locals():
                    st.write("ข้อมูลดิบจาก n8n:")
                    st.code(response.text)

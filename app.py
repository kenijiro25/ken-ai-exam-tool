import streamlit as st
import requests

st.set_page_config(page_title="P'Ken Exam Generator", layout="wide")
st.title("💡 เครื่องมือสร้างข้อสอบ Conversation โดย พี่เค็น")

context = st.text_area("1. วางบทสนทนาต้นฉบับที่นี่", height=250)
st.divider()

st.subheader("2. เลือกคำที่จะเจาะช่องว่าง (Fill in the blank)")
inputs = []
cols = st.columns(5) 
for i in range(5):
    with cols[i]:
        st.markdown(f"**คำถามข้อที่ {i+1}**")
        word = st.text_input(f"คำที่เลือก", key=f"w_{i}")
        category = st.selectbox(f"วัดเรื่อง", ["Tense", "Vocabulary", "Idiom", "Manner", "Logic"], key=f"c_{i}")
        inputs.append({"word": word, "type": category})

st.divider()

if st.button("🚀 Generate ข้อสอบ", type="primary", use_container_width=True):
    if not context or not any(item['word'] for item in inputs):
        st.warning("กรุณาใส่ข้อมูลให้ครบก่อนครับพี่เค็น")
    else:
        WEBHOOK_URL = "https://my-n8n-production-67b5.up.railway.app/webhook/create-exam" 
        payload = {"context": context, "inputs": inputs}
        
        with st.status("🤖 กำลังรอ AI หายเหนื่อยและส่งข้อสอบมานะครับ...", expanded=True) as status:
            try:
                response = requests.post(WEBHOOK_URL, json=payload)
                if response.status_code == 200:
                    try:
                        data = response.json()
                        # หยิบเนื้อหามาโชว์ (ไม่สนว่าชื่ออะไร)
                        exam_content = list(data.values())[0] if isinstance(data, dict) else data
                    except:
                        exam_content = response.text

                    if exam_content and len(exam_content) > 10:
                        status.update(label="✅ ดึงข้อมูลสำเร็จ!", state="complete", expanded=False)
                        st.success("ข้อสอบเจนเสร็จแล้วครับพี่เค็น!")
                        st.info(exam_content) # โชว์ในกล่องสีฟ้าเห็นชัดๆ
                        st.balloons()
                    else:
                        st.warning("AI ส่งค่าว่างกลับมา (โควตาอาจจะเต็ม) ลองใหม่ใน 1 นาทีครับพี่")
                else:
                    st.error(f"Error: n8n ติดขัด (รหัส {response.status_code})")
            except Exception as e:
                st.error(f"เชื่อมต่อไม่ได้: {e}")

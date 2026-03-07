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
        st.warning("กรุณาใส่ข้อมูลให้ครบครับพี่เค็น")
    else:
        WEBHOOK_URL = "https://my-n8n-production-67b5.up.railway.app/webhook/create-exam" 
        payload = {"context": context, "inputs": inputs}
        
        with st.status("🤖 กำลังแกะห่อข้อสอบให้พี่เค็นครับ...", expanded=True) as status:
            try:
                response = requests.post(WEBHOOK_URL, json=payload)
                if response.status_code == 200:
                    try:
                        data = response.json()
                        # สูตรแกะห่อ: พยายามหาชื่อ exam_text ถ้าไม่มีให้หยิบค่าแรกที่เจอมาเลย
                        if isinstance(data, dict):
                            exam_content = data.get("exam_text", list(data.values())[0])
                        else:
                            exam_content = data
                        
                        status.update(label="✅ ดึงข้อมูลสำเร็จ!", state="complete", expanded=False)
                        st.success("ข้อสอบเจนเสร็จแล้วครับพี่เค็น!")
                        st.divider()
                        st.markdown(exam_content) 
                        st.balloons()
                    except Exception as json_err:
                        st.error(f"แกะข้อมูลไม่ได้: {json_err} (ลองเช็คใน n8n ว่าใส่ exam_text= หรือยังครับ)")
                else:
                    st.error(f"Error: {response.status_code}")
            except Exception as e:
                st.error(f"เชื่อมต่อ n8n ไม่ได้: {e}")

import streamlit as st
import requests

# 1. ตั้งค่าหน้าจอ
st.set_page_config(page_title="P'Ken Exam Generator", layout="wide")
st.title("💡 เครื่องมือสร้างข้อสอบ Conversation โดย พี่เค็น")

# 2. ส่วนรับข้อมูล
context = st.text_area("1. วางบทสนทนาต้นฉบับที่นี่", height=250, placeholder="ใส่ Conversation ที่ต้องการ...")
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

# 3. ปุ่ม Generate
if st.button("🚀 Generate ข้อสอบ", type="primary", use_container_width=True):
    if not context or not any(item['word'] for item in inputs):
        st.warning("กรุณาใส่ข้อมูลให้ครบก่อนครับพี่เค็น")
    else:
        WEBHOOK_URL = "https://my-n8n-production-67b5.up.railway.app/webhook/create-exam" 
        payload = {"context": context, "inputs": inputs}
        
        with st.status("🤖 กำลังรอ AI ส่งข้อสอบกลับมานะครับ...", expanded=True) as status:
            try:
                response = requests.post(WEBHOOK_URL, json=payload)
                
                if response.status_code == 200:
                    status.update(label="✅ ได้รับข้อมูลจาก n8n แล้ว!", state="complete", expanded=False)
                    st.success("ข้อสอบเจนเสร็จแล้วครับพี่เค็น!")
                    st.divider()
                    
                    try:
                        # พยายามแกะ JSON
                        data = response.json()
                        if isinstance(data, dict):
                            # หยิบค่าแรกที่เจอมาโชว์ (ไม่สนว่าชื่ออะไร)
                            st.markdown(list(data.values())[0])
                        else:
                            st.markdown(data)
                    except:
                        # ถ้าไม่ใช่ JSON (เช่น ส่งมาเป็น Text เพียวๆ) ให้โชว์ตรงๆ เลย
                        st.markdown(response.text)
                        
                    st.balloons()
                else:
                    st.error(f"Error: n8n ตอบกลับด้วยรหัส {response.status_code}")
            except Exception as e:
                st.error(f"เชื่อมต่อไม่ได้: {e}")
                st.write("ข้อมูลดิบที่ได้รับ:")
                st.code(response.text if 'response' in locals() else "ไม่มีข้อมูลส่งออกมา")

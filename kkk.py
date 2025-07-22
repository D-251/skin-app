import openai
import streamlit as st

# إعداد الواجهة
st.set_page_config(page_title="تشخيص البشرة", layout="centered")
st.title("🧴 مساعد تشخيص مشاكل البشرة")

# إعداد مفتاح API من secrets
openai.api_key = st.secrets["api_key"]
openai.api_base = "https://openrouter.ai/api/v1"

# مدخلات المستخدم
gender = st.selectbox("👤 أنت:", ["أنثى", "ذكر"])
age = st.text_input("🎂 عمرك:")
symptoms = st.text_area("💬 اكتبي الأعراض اللي حاسة بيها في بشرتك:")

if st.button("🔍 شخّص الحالة"):
    with st.spinner("⏳ جاري تحليل الحالة..."):
        message = f"""
        أنا {gender}، عمري {age} سنة.
        أعاني من الأعراض التالية: {symptoms}.

        📌 شخص الحالة كطبيب أمراض جلدية محترف، وقدم التالي:
        1- التشخيص المبدئي.
        2- اسم منتج محلي (اسم تجاري معروف في مصر) لعلاج الحالة + السعر + صورة المنتج (رابط إن أمكن).
        3- اسم منتج غالي أو عالمي معروف + السعر + صورة.
        4- لو المنتجات غير متوفرة، قدّم بدائل حقيقية بالأسماء التجارية.
        """

        response = openai.ChatCompletion.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أنت طبيب أمراض جلدية محترف. قدم اقتراحات واضحة بناءً على السوق المصري."},
                {"role": "user", "content": message}
            ],
            temperature=0.2
        )

        response_text = response.choices[0].message["content"]
        st.markdown("### 🧴 التشخيص والاقتراح:")
        st.markdown(response_text)

        # عرض صور المنتجات
        product_images = {
            "بان أوكسيل": "https://i.imgur.com/LsGx4uc.jpg",
            "بنزاك": "https://i.imgur.com/VYx0clM.jpg",
            "ديفرين": "https://i.imgur.com/4tz6vPP.jpg",
            "ريتين-أ": "https://i.imgur.com/iT3eULe.jpg",
            "أكني فري": "https://i.imgur.com/9U8Vxjc.jpg",
            "إيزيس تين ديرم": "https://i.imgur.com/dRkgurZ.jpg"
        }

        st.markdown("### 📸 صور المنتجات المقترحة:")
        for name, url in product_images.items():
            if name.lower() in response_text.lower():
                st.image(url, caption=name, width=150)

# المتابعة
st.markdown("---")
st.markdown("### 🔁 هل استخدمت العلاج؟")
follow_up = st.text_area("📋 اكتب إذا حصل تحسن أو ظهرت أعراض جديدة:")

if st.button("📤 أرسل للمتابعة"):
    with st.spinner("⏳ جاري تعديل خطة العلاج بناءً على المتابعة..."):
        followup_msg = f"""
مريض استخدم العلاج، وكتب التالي:
"{follow_up}"

⏳ عدّل خطة العلاج بناءً على ذلك.
"""
        response2 = openai.ChatCompletion.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أنت طبيب تتابع الحالة بناءً على التطور."},
                {"role": "user", "content": followup_msg}
            ]
        )
        st.markdown("### 🔁 خطة العلاج بعد المتابعة:")
        st.markdown(response2.choices[0].message["content"])

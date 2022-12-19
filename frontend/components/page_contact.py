import streamlit


def contact_action():
    streamlit.title("Контакты по проекту")
    text = "### <div class='div_text'>" \
           "Лаборатория сорбционных процессов <br>" \
           "<br>Федеральное государственное бюджетное учреждение науки Институт физической химии и электрохимии им. " \
           "А.Н.Фрумкина Российской академии наук ИФХЭ РАН <br><br>" \
           "Email: knyazeva.mk@phyche.ac.ru " \
           "<br> Web: http://sorptionlab.ru - M.M.Dubinin Laboratory of sorption processes " \
           "https://adsorbtech.ru / - Engineering & Technical Center <br> <br>" \
           "Перейти на сайт института: https://www.phyche.ac.ru/</div>"
    streamlit.markdown(text, unsafe_allow_html=True)

import streamlit as st
import requests
import time

# Konfigurasi Halaman (Harus dipanggil paling atas)
st.set_page_config(
    page_title="Asesmen Literasi SD",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="collapsed"
)

def inject_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Lora:ital,wght@0,400;0,600;1,400&display=swap');
        
        /* Tipografi Utama */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        
        /* Desain Kotak Bacaan (Teks Cerita) */
        .reading-box {
            background-color: #f8fafc;
            border-left: 5px solid #0f172a;
            padding: 25px;
            border-radius: 0 10px 10px 0;
            font-family: 'Lora', serif;
            font-size: 1.1rem;
            line-height: 1.8;
            color: #334155;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        
        .reading-title {
            font-family: 'Inter', sans-serif;
            font-weight: 700;
            color: #0f172a;
            text-align: center;
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }

        /* Menyembunyikan menu Streamlit default untuk tampilan bersih */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Tombol Kustom */
        .stButton>button {
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
    </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# GANTI URL DI BAWAH INI DENGAN URL WEB APP GOOGLE SCRIPT ANDA
GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbxfCxwlUkn2eQxLGj1_hUH3vg_43u2WNhp6wnb1zItI8vwPVrcBvv4d1sQMGPT5cDS5/exec"

# Data Soal dan Kunci Jawaban
QUIZ_DATA = {
    "q1": {"type": "pg", "answer": "B. Susah dinasihati dan selalu memaksakan kehendaknya sendiri."},
    "q2": {"type": "pg", "answer": "B. Sombong dan suka menyombongkan diri"},
    "q3": {"type": "pg", "answer": "C. Peduli dan rela menolong makhluk yang sedang kesusahan."},
    "q4": {"type": "pgk", "answer": ["Bimo menjadi anak yang mau mendengarkan nasihat orang tuanya.", "Bimo menyadari kesalahannya dan tidak lagi bersikap sombong."]},
    "q5": {"type": "pg", "answer": "B. Kesombongan dan meremehkan nasihat orang lain dapat membawa kita pada bahaya."},
    "q6": {"type": "pg", "answer": "A. Karena ia dituntun oleh anak rusa yang sebelumnya telah ia tolong."},
    "q7": {"type": "pg", "answer": "A. Merasa paling hebat (sombong)."},
    "q8": {"type": "pgk", "answer": ["Doni adalah anak yang pemaaf meski sebelumnya telah diejek.", "Doni memiliki sifat peduli dan siap membantu teman."]},
    "q9": {"type": "pg", "answer": "C. Menganggap remeh atau merendahkan orang lain."},
    "q10": {"type": "pg", "answer": "B. Peristiwa layang-layang Riki yang putus dan tersangkut di pohon akibat angin."},
    "q11": {"type": "pg", "answer": "C. Riki menyadari kesalahannya, belajar menghargai, dan menjadi sahabat Doni."},
    "q12": {"type": "pg", "answer": "B. Nilai tolong-menolong tanpa pamrih dan kebesaran hati untuk memaafkan."}
}

if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'user_name' not in st.session_state:
    st.session_state.user_name = ''
if 'user_school' not in st.session_state:
    st.session_state.user_school = ''
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'submit_status' not in st.session_state:
    st.session_state.submit_status = ""

def login_page():
    st.markdown("<h1 style='text-align: center; color: #0f172a;'>Pusat Asesmen Literasi SD</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b;'>Kompetensi: Pemahaman Inferensial (Teks Fiksi)</p>", unsafe_allow_html=True)
    st.write("---")
    
    st.markdown("### Identitas Peserta")
    name = st.text_input("Nama Lengkap", placeholder="Masukkan nama Anda...")
    school = st.text_input("Asal Sekolah", placeholder="Contoh: SDN Merdeka 01")
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.write("") # Spacer
        if st.button("Mulai Latihan Kuis", use_container_width=True, type="primary"):
            if name.strip() == "" or school.strip() == "":
                st.error("⚠️ Nama dan Asal Sekolah wajib diisi!")
            else:
                st.session_state.user_name = name
                st.session_state.user_school = school
                st.session_state.page = 'quiz'
                st.rerun()

def render_text_1():
    st.markdown("""
    <div class="reading-box">
        <div class="reading-title">Petualangan Bimo di Hutan Damar</div>
        <p>Di pinggir desa yang asri, berbatasan langsung dengan Hutan Damar yang sangat lebat, tinggallah seorang anak laki-laki berusia sepuluh tahun bernama Bimo. Bimo dikenal oleh teman-temannya sebagai anak yang <em>kepala batu</em>. Jika ia sudah menginginkan atau meyakini sesuatu, tidak ada seorang pun yang bisa menasihati atau melarangnya. Suatu hari, Bimo mendengar cerita dari teman-teman sekelasnya tentang bunga anggrek bercahaya yang konon hanya mekar setiap sepuluh tahun sekali di bagian paling tengah Hutan Damar. Teman-temannya hanya berani bercerita dari mulut ke mulut, tetapi sama sekali tidak ada yang berani masuk ke sana karena hutan itu sangat luas, gelap, dan menyesatkan. Namun, Bimo merasa dirinya adalah anak yang paling berani dan hebat. "Ah, hutan begini saja kalian sudah ketakutan. Aku akan masuk dan membawa bunga itu ke desa besok pagi supaya kalian tahu siapa yang paling hebat!" ucap Bimo dengan sifat <em>besar kepala</em>.</p>
        <p>Keesokan harinya, sesaat sebelum matahari terbit, Bimo menyelinap masuk ke dalam Hutan Damar dengan membawa bekal seadanya. Ia berjalan dengan langkah gagah, menyusuri jalan setapak yang ditutupi oleh lumut hijau yang licin. Awalnya, perjalanan tersebut terasa sangat menyenangkan. Namun, setelah berjalan tanpa henti selama lebih dari tiga jam, suasana mulai berubah drastis. Pohon-pohon menjulang semakin tinggi dan jarak antarpohon semakin rapat. Sinar matahari yang tadinya terang benderang kini hanya bisa menyusup sedikit, membuat suasana hutan menjadi remang-remang. Bimo mulai kebingungan. Ia mencoba kembali berbalik arah, tetapi setiap jalan terlihat sama persis. Jantungnya berdebar kencang tak karuan. Ia menyadari bahwa kesombongannya telah membawanya ke dalam masalah besar.</p>
        <p>Di tengah rasa putus asa, Bimo tiba-tiba mendengar suara gemerisik dari balik semak-semak. Ia merinding dan bersembunyi di balik pohon mahoni. Ternyata, sumber suara itu adalah seekor anak rusa yang kakinya terjepit kuat di antara akar pohon beringin tua. Melihat rusa kecil itu merintih kesakitan, sifat asli Bimo yang sebenarnya sangat peduli pada hewan pun muncul. Ia seketika lupa pada rasa takutnya sendiri. Dengan sangat hati-hati, Bimo mendekat dan merenggangkan akar tersebut hingga kaki rusa terlepas. Rusa itu menatap Bimo sejenak, lalu berjalan pincang ke suatu arah sambil sesekali menengok ke belakang, seolah-olah mengajak Bimo untuk mengikutinya.</p>
        <p>Karena sudah tidak punya pilihan arah yang lain, Bimo memutuskan mengikuti rusa tersebut. Ajaibnya, rusa kecil itu menuntun Bimo melewati rute yang aman, hingga akhirnya berujung di pinggir sungai batas desanya saat hari mulai gelap. Di ujung jalan, rusa itu menghilang. Bimo <em>menghela napas panjang</em>, merasa sangat bersyukur bisa kembali dengan selamat berkat bantuan rusa yang ditolongnya. Semenjak kejadian hari itu, Bimo berubah drastis. Ia tidak lagi sombong dan mulai mendengarkan nasihat dari orang tuanya. Bimo sadar bahwa meremehkan peringatan orang lain bisa berakibat fatal bagi dirinya.</p>
    </div>
    """, unsafe_allow_html=True)

def render_text_2():
    st.markdown("""
    <div class="reading-box">
        <div class="reading-title">Kisah Layang-Layang Putus di Desa Sukamaju</div>
        <p>Sore itu, langit di atas lapangan Desa Sukamaju dihiasi oleh puluhan layang-layang berbagai warna dan ukuran. Angin berembus cukup kencang dari arah selatan. Di sudut lapangan, terlihat Riki sedang sibuk mengulur benang gelasan miliknya. Layang-layang merah bergambar naga milik Riki terbang paling tinggi dan gagah di antara yang lain. Di sebelahnya, ada Doni yang sedang memegang layang-layang biru sederhana yang terbuat dari kertas koran bekas. Doni tampak bersedih karena layang-layangnya tidak bisa terbang dengan stabil, selalu saja oleng ke kanan dan ke kiri lalu menukik tajam ke tanah.</p>
        <p>"Makanya, Don, kalau buat layang-layang itu rangkanya harus seimbang. Jangan asal ikat saja. Lihat punyaku, terbang anteng seperti burung elang," ledek Riki sambil tersenyum <em>tinggi hati</em>. Doni hanya diam mendengarnya. Ia sadar bahwa layang-layangnya memang jelek karena ia merakitnya sendiri dari barang-barang bekas, tidak seperti layang-layang milik Riki yang dibeli dari toko mainan paling mahal.</p>
        <p>Beberapa saat kemudian, angin tiba-tiba bertiup dengan sangat kencang. Banyak anak kesulitan mengendalikan tarikannya. Layang-layang naga milik Riki mulai bergerak liar. Riki panik dan menarik benang gelasannya terlalu kuat. "Krak!" Benang gelasan yang tipis itu pun putus. Layang-layang merah kebanggaan Riki terbang tanpa arah, terbawa angin kencang hingga akhirnya tersangkut kuat di dahan pohon mangga yang paling tinggi di pinggir lapangan. Riki hampir menangis melihat hal itu. Ia berlari ke bawah pohon, tetapi pohonnya terlalu licin untuk dipanjat.</p>
        <p>Melihat Riki yang sedang bersedih, Doni tidak tinggal diam. Ia segera berlari pulang ke rumahnya yang tidak jauh dari lapangan. Tak lama kemudian, Doni kembali membawa sebatang galah bambu yang sangat panjang. Doni berusaha keras menjangkau benang layang-layang Riki dengan ujung bambu tersebut. Setelah keringat bercucuran, ujung galah akhirnya berhasil mengait benang itu. Dengan sangat hati-hati agar kertasnya tidak sobek, Doni menariknya turun.</p>
        <p>Riki menatap Doni dengan perasaan campur aduk. Ia merasa sangat malu karena sebelumnya telah mengejek hasil karya sahabatnya itu. "Doni, terima kasih banyak ya. Maafkan aku, tadi aku sudah <em>memandang sebelah mata</em> padamu dan mengejek layang-layang buatanmu," ucap Riki dengan suara pelan sambil menunduk menyesal. "Tidak apa-apa, Riki. Kita kan berteman, sudah seharusnya saling membantu," jawab Doni tersenyum tulus.</p>
    </div>
    """, unsafe_allow_html=True)

def quiz_page():
    st.title(f"Halo, {st.session_state.user_name} 👋")
    st.info("Bacalah teks dengan saksama, lalu jawab pertanyaannya. Jika soal meminta lebih dari satu jawaban, pilih semua yang benar.")
    
    with st.form("quiz_form"):
        # TEKS 1
        st.write("---")
        render_text_1()
        
        st.subheader("Soal 1")
        q1 = st.radio("Pada paragraf pertama, Bimo dideskripsikan sebagai anak yang 'kepala batu'. Apa makna dari ungkapan tersebut?", 
                      ["A. Anak yang sangat cerdas dalam memahami pelajaran sekolah.", "B. Susah dinasihati dan selalu memaksakan kehendaknya sendiri.", "C. Memiliki fisik yang sangat kuat saat menjelajah hutan.", "D. Anak yang selalu bersikap ramah dan sopan kepada teman."], index=None)
        
        st.subheader("Soal 2")
        q2 = st.radio("Saat berbicara kepada teman-temannya di paragraf pertama, Bimo mengucapkan kalimat dengan sifat 'besar kepala'. Apa arti ungkapan tersebut?", 
                      ["A. Penakut dan mudah menyerah", "B. Sombong dan suka menyombongkan diri", "C. Pemberani dan pantang mundur", "D. Sabar dalam menghadapi cobaan"], index=None)
        
        st.subheader("Soal 3")
        q3 = st.radio("Meskipun Bimo dikenal sombong, dapat disimpulkan bahwa ia memiliki watak tersembunyi yang baik. Berdasarkan peristiwa di paragraf ketiga, apa watak asli Bimo tersebut?", 
                      ["A. Mudah putus asa saat tersesat di kegelapan hutan.", "B. Gemar berburu binatang liar di dalam hutan.", "C. Peduli dan rela menolong makhluk yang sedang kesusahan.", "D. Sabar menunggu bunga anggrek bercahaya mekar."], index=None)
        
        st.subheader("Soal 4 (Pilihan Ganda Kompleks)")
        q4 = st.multiselect("Bagaimana simpulan perubahan sifat Bimo setelah berhasil keluar dari Hutan Damar? (Pilih jawaban benar, lebih dari 1)", 
                            ["Bimo menjadi anak yang mau mendengarkan nasihat orang tuanya.", "Bimo semakin sering meremehkan peringatan dari teman-temannya.", "Bimo menyadari kesalahannya dan tidak lagi bersikap sombong.", "Bimo menjadi anak yang penakut dan mengurung diri di rumah."])
        
        st.subheader("Soal 5")
        q5 = st.radio("Apa pesan moral utama yang dapat diambil dari kisah petualangan Bimo tersebut?", 
                      ["A. Kita harus selalu membawa bekal makanan yang banyak saat bermain di luar.", "B. Kesombongan dan meremehkan nasihat orang lain dapat membawa kita pada bahaya.", "C. Hewan liar di hutan sebaiknya tidak boleh didekati oleh anak-anak.", "D. Jangan pernah percaya pada cerita tentang bunga yang bisa bercahaya."], index=None)
        
        st.subheader("Soal 6")
        q6 = st.radio("Dari kejadian di dalam teks, mengapa akhirnya Bimo bisa selamat dan menemukan jalan pulang ke desa?", 
                      ["A. Karena ia dituntun oleh anak rusa yang sebelumnya telah ia tolong.", "B. Karena ia mengingat kembali jalan masuk melalui lumut hijau.", "C. Karena ia mengikuti arah sinar matahari terbenam.", "D. Karena teman-temannya menyusul ke dalam hutan."], index=None)

        # TEKS 2
        st.write("---")
        render_text_2()

        st.subheader("Soal 7")
        q7 = st.radio("Pada paragraf kedua, Riki meledek Doni sambil tersenyum 'tinggi hati'. Apa makna dari ungkapan tersebut?", 
                      ["A. Merasa paling hebat (sombong).", "B. Merasa sangat gembira.", "C. Merasa sabar dan ikhlas.", "D. Merasa sangat cerdas."], index=None)

        st.subheader("Soal 8 (Pilihan Ganda Kompleks)")
        q8 = st.multiselect("Berdasarkan tindakan yang dilakukannya saat layangan Riki putus, kesimpulan apa yang tepat mengenai watak Doni? (Pilih jawaban benar, lebih dari 1)", 
                            ["Doni suka membalas dendam saat temannya kesusahan.", "Doni adalah anak yang pemaaf meski sebelumnya telah diejek.", "Doni iri hati terhadap mainan mahal milik orang lain.", "Doni memiliki sifat peduli dan siap membantu teman."])

        st.subheader("Soal 9")
        q9 = st.radio("Di akhir cerita, Riki menyesal karena telah 'memandang sebelah mata' pada Doni. Arti ungkapan tersebut adalah...", 
                      ["A. Melihat dengan cara memejamkan satu mata.", "B. Memperhatikan pekerjaan orang lain dengan sangat teliti.", "C. Menganggap remeh atau merendahkan orang lain.", "D. Mengagumi hasil karya yang dibuat oleh teman."], index=None)

        st.subheader("Soal 10")
        q10 = st.radio("Apa gagasan utama yang diceritakan pada paragraf ketiga teks tersebut?", 
                      ["A. Riki berhasil membuat layang-layang baru dari bambu.", "B. Peristiwa layang-layang Riki yang putus dan tersangkut di pohon akibat angin.", "C. Teman-teman di lapangan membantu Riki memanjat pohon mangga.", "D. Doni merasa sangat senang melihat layang-layang mahal milik Riki rusak."], index=None)

        st.subheader("Soal 11")
        q11 = st.radio("Bagaimana simpulan perubahan karakter Riki terhadap Doni di akhir cerita?", 
                      ["A. Riki tetap mengejek layang-layang Doni yang terbuat dari koran.", "B. Riki semakin sombong dan memutuskan untuk menjauhi Doni.", "C. Riki menyadari kesalahannya, belajar menghargai, dan menjadi sahabat Doni.", "D. Riki marah karena Doni menggunakan galah bambu milik ayahnya."], index=None)

        st.subheader("Soal 12")
        q12 = st.radio("Nilai kehidupan apa yang paling menonjol dan dapat diteladani dari sikap Doni dalam cerita tersebut?", 
                      ["A. Nilai kejujuran dalam membeli barang di toko mainan.", "B. Nilai tolong-menolong tanpa pamrih dan kebesaran hati untuk memaafkan.", "C. Nilai kedisiplinan dan keberanian memanjat pohon.", "D. Nilai ketekunan dalam merakit layang-layang agar terbang tinggi."], index=None)

        st.write("---")
        submit = st.form_submit_button("✅ Koreksi & Kirim Jawaban", use_container_width=True)

        if submit:
            # Validation
            answers = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12]
            if None in answers or [] in answers:
                st.error("Peringatan: Harap jawab seluruh 12 pertanyaan sebelum mengumpulkan!")
            else:
                correct_count = 0
                total_q = 12
                
                # Grade logic
                if q1 == QUIZ_DATA["q1"]["answer"]: correct_count += 1
                if q2 == QUIZ_DATA["q2"]["answer"]: correct_count += 1
                if q3 == QUIZ_DATA["q3"]["answer"]: correct_count += 1
                if sorted(q4) == sorted(QUIZ_DATA["q4"]["answer"]): correct_count += 1
                if q5 == QUIZ_DATA["q5"]["answer"]: correct_count += 1
                if q6 == QUIZ_DATA["q6"]["answer"]: correct_count += 1
                if q7 == QUIZ_DATA["q7"]["answer"]: correct_count += 1
                if sorted(q8) == sorted(QUIZ_DATA["q8"]["answer"]): correct_count += 1
                if q9 == QUIZ_DATA["q9"]["answer"]: correct_count += 1
                if q10 == QUIZ_DATA["q10"]["answer"]: correct_count += 1
                if q11 == QUIZ_DATA["q11"]["answer"]: correct_count += 1
                if q12 == QUIZ_DATA["q12"]["answer"]: correct_count += 1

                final_score = round((correct_count / total_q) * 100)
                st.session_state.score = final_score

                # Send data to Google Sheets via webhook
                with st.spinner("https://script.google.com/macros/s/AKfycbwW8PYd0-Q8SNThyi59vK55oL6ZKMv4SNBgX6P_-0fiRs6dI2R7cNl_WrvOzXIvF6OZ/exec"):
                    try:
                        payload = {
                            "nama": st.session_state.user_name,
                            "sekolah": st.session_state.user_school,
                            "skor": final_score
                        }
                        response = requests.post(GOOGLE_SHEET_URL, data=payload)
                        if response.status_code == 200:
                            st.session_state.submit_status = "Sukses"
                        else:
                            st.session_state.submit_status = "Gagal HTTP"
                    except Exception as e:
                        st.session_state.submit_status = f"Gagal Error: {e}"

                st.session_state.page = 'result'
                st.rerun()

def result_page():
    st.balloons()
    st.markdown("<h1 style='text-align: center; color: #10b981;'>Latihan Selesai!</h1>", unsafe_allow_html=True)
    st.write(f"**Nama:** {st.session_state.user_name} | **Sekolah:** {st.session_state.user_school}")
    
    st.metric(label="Skor Akhir Anda", value=f"{st.session_state.score} / 100")
    
    if st.session_state.submit_status == "Sukses":
        st.success("✅ Nilai Anda berhasil tersimpan di sistem Google Sheets Guru/Admin.")
    else:
        st.warning(f"⚠️ Gagal menyimpan ke sistem daring. Error: {st.session_state.submit_status}")

    st.write("---")
    st.markdown("### 📖 Pembahasan Lengkap")
    
    with st.expander("Lihat Pembahasan Soal 1-6 (Petualangan Bimo)"):
        st.write("**Soal 1:** B (Kepala batu = susah dinasihati/keras kepala)")
        st.write("**Soal 2:** B (Besar kepala = sombong/congkak)")
        st.write("**Soal 3:** C (Bimo peduli dan rela menolong anak rusa yang terjepit akar)")
        st.write("**Soal 4 (PGK):** Bimo mulai mendengarkan nasihat orang tua & menyadari kesalahannya. Paragraf terakhir membuktikan Bimo berubah drastis menjadi tidak sombong.")
        st.write("**Soal 5:** B (Pesan moral utama: kesombongan membawa kita pada masalah besar)")
        st.write("**Soal 6:** A (Bimo dituntun keluar hutan oleh rusa yang diselamatkannya)")

    with st.expander("Lihat Pembahasan Soal 7-12 (Kisah Layang-Layang)"):
        st.write("**Soal 7:** A (Tinggi hati = sombong/merasa paling hebat)")
        st.write("**Soal 8 (PGK):** Doni pemaaf meski diejek & sangat peduli siap membantu teman. Terbukti ia berlari pulang mengambil galah bambu untuk Riki.")
        st.write("**Soal 9:** C (Memandang sebelah mata = meremehkan/menganggap enteng orang lain)")
        st.write("**Soal 10:** B (Gagasan utama paragraf 3: Angin kencang membuat layangan Riki putus lalu nyangkut di pohon)")
        st.write("**Soal 11:** C (Riki malu, minta maaf, belajar menghargai dan akhirnya bersahabat dengan Doni)")
        st.write("**Soal 12:** B (Nilai moral dari Doni: Kebesaran hati memaafkan ejekan dan ikhlas tolong-menolong)")

    if st.button("Ulangi Latihan", type="secondary"):
        st.session_state.page = 'login'
        st.session_state.score = 0
        st.rerun()

if st.session_state.page == 'login':
    login_page()
elif st.session_state.page == 'quiz':
    quiz_page()
elif st.session_state.page == 'result':
    result_page()

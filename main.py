import io
from flask import Flask
from flask import send_file
from flask import request
from flask import render_template
from KnapsackPSO import Knapsack_PSO
import matplotlib.pyplot as plt
import base64

app = Flask(__name__)
@app.route("/")
def index():
    data_barang = [
        ["Furadan 2 kg", 2, 10, 19500, 30500],
        ["Amegrass 10 kg", 10, 4, 55000, 67500],
        ["Polaram 1 kg", 1, 16, 60000, 68000],
        ["Plastik mulsa 18 kg", 18, 2, 730000, 790000],
        ["Topsin M 500 g", 0.5, 20, 62000, 75000],
        ["Klopindo 100 g", 0.1, 10, 15000, 23000],
        ["Lannate Biru 100 g", 0.1, 10, 25000, 29000],
        ["Lannate Merah 100 g", 0.1, 20, 20000, 27000],
        ["Lannate Merah 15 g", 0.015, 40, 15000, 25000],
        ["Furadan 3 gr 1kg", 1, 10, 16000, 24500],
        ["Metindo 25 wp 100 g", 0.1, 20, 27500, 35000],
        ["Confidor 100 g", 0.1, 10, 26000, 31500],
        ["Dangke 100 g", 0.1, 10, 15000, 20500],
        ["Dangke 40 WP 250 gr", 0.25, 20, 42000, 55000],
        ["Plastik mulsa 9 kg", 9, 5, 305000, 350000],
        ["Plastik mulsa 15 kg", 15, 4, 457000, 500000],
        ["Amegrass 5 kg", 5, 10, 315000, 350000],
        ["Teku 100 EC 100 g", 0.1, 50, 21000, 30000],
        ["Teku 100 EC 200 g", 0.2, 40, 38000, 45000],
        ["Teku 100 EC 400 g", 0.4, 20, 72500, 80000],
        ["Crowen 113 EC 80 g", 0.08, 50, 13000, 20000],
        ["Crowen 113 EC 200 g", 0.2, 40, 23500, 30000],
        ["Crowen 113 EC 400 g", 0.4, 20, 40000, 49500],
        ["Dithane 200 g", 0.2, 15, 17000, 24000],
        ["Antracol 250 g", 0.25, 18, 30500, 35000],
        ["Antracol 500 g", 0.5, 12, 52000, 60000],
        ["Benstar 200 g", 0.2, 22, 18000, 23000],
        ["Masalgin 200 g", 0.2, 14, 16000, 20000],
        ["Phycozan 200 g", 0.2, 17, 16000, 21000],
        ["Acrobat 10 g", 0.01, 20, 8000, 12000],
        ["Acrobat 40 g", 0.04, 6, 30000, 37000],
        ["Gandsi. D 500 g", 0.5, 10, 22500, 28000],
        ["Gandsi. B 500 g", 0.5, 15, 21000, 30500],
        ["Ridomild gold 100 g", 0.1, 50, 24500, 30000],
        ["Saromyl 25 g", 0.025, 20, 27500, 35000],
        ["Saromyl 5 g", 0.005, 50, 8500, 12000],
        ["Procure 400 g", 0.4, 17, 41000, 50000],
        ["Starmyl 100 g", 0.1, 32, 48000, 59000],
        ["Dense 200 g", 0.2, 12, 30000, 38000],
        ["BM Toplas 100 g", 0.1, 20, 14500, 20000],
        ["BM Zebco 1 kg", 1, 5, 52000, 64000]
    ]
    return render_template("index.html", data=data_barang)

@app.route("/result", methods=["GET", "POST"])
def result():
    if request.method == "POST":
        banyakKasus = request.form.get('banyakkasus')
        kasusPopulasi = request.form.getlist('partikel')
        namabarang = request.form.getlist('namabarang')
        beratbarang = request.form.getlist('beratbarang')
        banyakbarang = request.form.getlist('banyakbarang')
        hargabeli = request.form.getlist('hargabeli')
        hargajual = request.form.getlist('hargajual')

        nama_barang = []
        data = []

        for i in range(len(namabarang)):
            nama_barang.append(namabarang[i])
            data.append([round(float(beratbarang[i]) * int(banyakbarang[i]), 3), (int(hargajual[i]) - int(hargabeli[i])) * int(banyakbarang[i])])

        maxKnapsack = int(request.form.get('maxKnapsack'))
        iterasi = int(request.form.get('iterasi'))


        result = []
        barangTerpilih = []
        recent = []

        fig, ax = plt.subplots()

        for i in range(len(kasusPopulasi)):
            pso = Knapsack_PSO(data=data, maxKnapsack=maxKnapsack, iterasi=int(iterasi), pop_size=int(kasusPopulasi[i]))
            pso.run()
            tempX = []
            tempY = []
            for k in pso.history:
                tempX.append(k[0])
                tempY.append(k[1][0])
            recent.append([tempX, tempY])
            tempBarangTerpilih = []
            for j in range(len(pso.gBest[1])):
                if pso.gBest[1][j] == '1':
                    tempBarangTerpilih.append(nama_barang[j])
            barangTerpilih.append([kasusPopulasi[i], tempBarangTerpilih])
            result.append([kasusPopulasi[i], pso.gBest])

        # Buat plot Matplotlib
        for i in recent:
            ax.plot(i[0], i[1])
        ax.grid(True)
        ax.set_title('Hasil Grafik')
        ax.set_xlabel('Iterasi')
        ax.set_ylabel('Fitness')

        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        plot_url = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close(fig)
        return render_template("result.html", result=result, barangTerpilih=barangTerpilih, jumlahData=len(result), plot_url=plot_url, recent=recent, lenRecent=len(recent[0]), kasusPopulasi=kasusPopulasi)
    return "Error"

# @app.route("/about")
# def about():
#     return "<h1>About</h1>"

# @app.route("/profile/<username>")
# def profile(username):
#     return f"<h1>{username}</h1>"

# @app.route("/cobarequest", methods=["POST", "GET"])
# def cobarequest():
#     if request.method == "POST":
#         return f"<h1>POST</h1>"
#     else:
#         return f"<h1>GET</h1>"

app.run(debug=True)

# [
#     [
#         [x], [y]
#     ]
# ]
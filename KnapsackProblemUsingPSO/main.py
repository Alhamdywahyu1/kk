from flask import Flask, request, render_template, redirect, url_for, session, send_file
import os
import io
import matplotlib.pyplot as plt
from KnapsackPSO import Knapsack_PSO

app = Flask(__name__)
app.secret_key = 'knapsack_secret_key'

# Helper untuk inisialisasi data item di session

def get_items():
    if 'items' not in session:
        session['items'] = []
    return session['items']

def set_items(items):
    session['items'] = items

@app.route('/', methods=['GET', 'POST'])
def index():
    items = get_items()
    result = None
    if request.method == 'POST':
        # Tambah item
        if 'add_item' in request.form:
            berat = float(request.form['berat'])
            nilai = float(request.form['nilai'])
            items.append([berat, nilai])
            set_items(items)
        # Edit item
        elif 'edit_item' in request.form:
            idx = int(request.form['edit_index'])
            berat = float(request.form['edit_berat'])
            nilai = float(request.form['edit_nilai'])
            items[idx] = [berat, nilai]
            set_items(items)
        # Hapus item
        elif 'delete_item' in request.form:
            idx = int(request.form['delete_index'])
            items.pop(idx)
            set_items(items)
        # Jalankan PSO
        elif 'run_pso' in request.form:
            maxKnapsack = float(request.form['maxKnapsack'])
            iterasi = int(request.form['iterasi'])
            pop_size = int(request.form['pop_size'])
            if len(items) > 0:
                pso = Knapsack_PSO(items, maxKnapsack, iterasi, pop_size)
                pso.run()
                # Simpan hasil ke session
                session['result'] = {
                    'gBest': pso.gBest,
                    'history': pso.history,
                    'maxKnapsack': maxKnapsack,
                    'items': items
                }
                return redirect(url_for('result'))
    return render_template('index.html', items=items)

@app.route('/result')
def result():
    result = session.get('result', None)
    if not result:
        return redirect(url_for('index'))
    # Data untuk tabel hasil
    gBest = result['gBest']
    items = result['items']
    maxKnapsack = result['maxKnapsack']
    # Hitung total berat dan nilai dari solusi terbaik
    if gBest[1]:
        selected = [int(x) for x in gBest[1]]
        total_berat = sum(items[i][0] for i in range(len(items)) if selected[i])
        total_nilai = sum(items[i][1] for i in range(len(items)) if selected[i])
        selected_items = [(i+1, items[i][0], items[i][1]) for i in range(len(items)) if selected[i]]
    else:
        total_berat = 0
        total_nilai = 0
        selected_items = []
    return render_template('result.html', gBest=gBest, total_berat=total_berat, total_nilai=total_nilai, maxKnapsack=maxKnapsack, selected_items=selected_items)

@app.route('/fitness_plot')
def fitness_plot():
    result = session.get('result', None)
    if not result:
        return redirect(url_for('index'))
    history = result['history']
    generations = [h[0] for h in history]
    fitness = [h[1][0] if h[1][0] is not None else 0 for h in history]
    plt.figure(figsize=(6,4))
    plt.plot(generations, fitness, marker='o')
    plt.title('Fitness Terbaik per Generasi')
    plt.xlabel('Generasi')
    plt.ylabel('Fitness')
    plt.tight_layout()
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    # Production ready - bisa berjalan di cloud hosting
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
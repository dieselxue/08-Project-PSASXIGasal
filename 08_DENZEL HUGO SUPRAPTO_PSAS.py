import tkinter as tk
from tkinter import ttk

data_pemesanan = []
current_frame = None
frames = {}
root = tk.Tk()
root.title("Aplikasi Pemesanan Tiket Pesawat")
root.geometry("800x600")
container = tk.Frame(root)
container.pack()

def tampilkan_halaman(page_name):
    global current_frame
    if current_frame:
        current_frame.pack_forget()
    current_frame = frames[page_name]
    current_frame.pack()

def tambah_data(data):
    data_pemesanan.append(data)
    return True

def cari_data(nama_penumpang):
    hasil = []
    for data in data_pemesanan:
        if nama_penumpang.lower() in data['nama_penumpang'].lower():
            hasil.append(data)
    return hasil

def hitung_total_pendapatan():
    total = 0
    for data in data_pemesanan:
        total += data['harga_tiket']
    return total

def buat_halaman_utama():
    frame = tk.Frame(container)
    tk.Label(frame, text="Aplikasi Pemesanan Tiket Pesawat", font=("Merriweather", 16)).pack()
    tk.Label(frame, text="Silakan pilih menu:").pack()
    tk.Button(frame, text="Form Input Data", width=20, height=2, command=lambda: tampilkan_halaman("input")).pack()
    tk.Button(frame, text="Tampil Data", width=20, height=2, command=lambda: tampilkan_halaman("tampil")).pack()
    tk.Button(frame, text="Pencarian Data", width=20, height=2, command=lambda: tampilkan_halaman("cari")).pack()
    tk.Button(frame, text="Hasil / Laporan", width=20, height=2, command=lambda: tampilkan_halaman("laporan")).pack()
    return frame

def buat_form_input():
    frame = tk.Frame(container)
    tk.Label(frame, text="Form Input Data Pemesanan", font=("Merriweather", 14)).pack()
    status_label = tk.Label(frame, text="")
    status_label.pack()
    tk.Label(frame, text="Nama Penumpang:").pack()
    entry_nama = tk.Entry(frame, width=30)
    entry_nama.pack()
    tk.Label(frame, text="Umur:").pack()
    entry_umur = tk.Entry(frame, width=30)
    entry_umur.pack()
    tk.Label(frame, text="Harga Tiket:").pack()
    entry_harga = tk.Entry(frame, width=30)
    entry_harga.pack()
    tk.Label(frame, text="Kelas Penerbangan:").pack()
    combo_kelas = ttk.Combobox(frame, values=["Ekonomi", "Bisnis", "First Class"], width=27)
    combo_kelas.pack()
    tk.Label(frame, text="Pemesanan Makanan:").pack()
    var_meal = tk.BooleanVar()
    tk.Checkbutton(frame, variable=var_meal).pack()
  
    def simpan_data():
        status_label.config(text="")
        try:
            nama = entry_nama.get()
            umur = int(entry_umur.get())
            harga = float(entry_harga.get())
            kelas = combo_kelas.get()
            meal = var_meal.get()
            if not nama:
                status_label.config(text="Tolong nama diisi.")
                return
            if umur <= 0:
                status_label.config(text="Umur harus lebih dari 0.")
                return
            if harga <= 0:
                status_label.config(text="Harga harus lebih dari 0.")
                return
            if not kelas:
                status_label.config(text="Tolong pilih kelas.")
                return
            data = {'nama_penumpang': nama, 'umur': umur, 'harga_tiket': harga, 'kelas': kelas, 'meal': meal}
            if tambah_data(data):
                status_label.config(text="Data berhasil ditambahkan.")
                entry_nama.delete(0, tk.END)
                entry_umur.delete(0, tk.END)
                entry_harga.delete(0, tk.END)
                combo_kelas.set('')
                var_meal.set(False)
        except ValueError:
            status_label.config(text="Umur dan harga harus angka.")
          
    tk.Button(frame, text="Simpan Data", width=15, command=simpan_data).pack()
    tk.Button(frame, text="Kembali", width=15, command=lambda: tampilkan_halaman("utama")).pack()
    return frame

def buat_tampil_data():
    frame = tk.Frame(container)
    tk.Label(frame, text="Tampilan Data Pemesanan", font=("Merriweather", 14)).pack()
    info_label = tk.Label(frame, text="")
    info_label.pack()
    table_frame = tk.Frame(frame)
    table_frame.pack()
    columns = ("Nama", "Umur", "Harga", "Kelas", "Makanan")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left")
    scrollbar.pack(side="right", fill="y")
    
    def refresh_data():
        for item in tree.get_children():
            tree.delete(item)
        for data in data_pemesanan:
            tree.insert("", "end", values=( data['nama_penumpang'], data['umur'], f"Rp {data['harga_tiket']:,.0f}", data['kelas'], "Ya" if data['meal'] else "Tidak"))
        info_label.config(text=f"Total: {len(data_pemesanan)} data")
    
    tk.Button(frame, text="Refresh Data", width=15, command=refresh_data).pack()
    tk.Button(frame, text="Kembali", width=15, command=lambda: tampilkan_halaman("utama")).pack()
    refresh_data()
    return frame

def buat_pencarian_data():
    frame = tk.Frame(container)
    tk.Label(frame, text="Pencarian Data Pemesanan", font=("Merriweather", 14)).pack()
    info_label = tk.Label(frame, text="")
    info_label.pack()
    search_frame = tk.Frame(frame)
    search_frame.pack()
    tk.Label(search_frame, text="Cari nama:").pack(side="left")
    entry_cari = tk.Entry(search_frame, width=30)
    entry_cari.pack(side="left")
    result_frame = tk.Frame(frame)
    result_frame.pack()
    columns = ("Nama", "Umur", "Harga", "Kelas", "Makanan")
    tree = ttk.Treeview(result_frame, columns=columns, show="headings", height=8)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left")
    scrollbar.pack(side="right", fill="y")
    
    def cari_data_handler():
        for item in tree.get_children():
            tree.delete(item)
        nama = entry_cari.get()
        if nama:
            hasil = cari_data(nama)
            for data in hasil:
                tree.insert("", "end", values=(data['nama_penumpang'], data['umur'], f"Rp {data['harga_tiket']:,.0f}", data['kelas'], "Ya" if data['meal'] else "Tidak"))
            info_label.config(text=f"Ditemukan {len(hasil)} hasil")
        else:
            info_label.config(text="Masukkan nama!")
    tk.Button(search_frame, text="Cari", width=10, command=cari_data_handler).pack(side="left")
    tk.Button(frame, text="Kembali", width=15, command=lambda: tampilkan_halaman("utama")).pack()
    return frame

def buat_hasil_laporan():
    frame = tk.Frame(container)
    tk.Label(frame, text="Laporan dan Perhitungan", font=("Merriweather", 14)).pack()
    label_jumlah = tk.Label(frame, text="Jumlah Pemesanan: 0")
    label_jumlah.pack()
    label_pendapatan = tk.Label(frame, text="Total Pendapatan: Rp 0")
    label_pendapatan.pack()
    label_rata_harga = tk.Label(frame, text="Rata-Rata Harga: Rp 0")
    label_rata_harga.pack()
    tk.Label(frame, text="Distribusi Kelas:", font=("Merriweather", 12)).pack()
    kelas_frame = tk.Frame(frame)
    kelas_frame.pack()
    label_ekonomi = tk.Label(kelas_frame, text="Ekonomi: 0")
    label_ekonomi.pack(side="left")
    label_bisnis = tk.Label(kelas_frame, text="Bisnis: 0")
    label_bisnis.pack(side="left")
    label_first = tk.Label(kelas_frame, text="First Class: 0")
    label_first.pack(side="left")
    label_meal = tk.Label(frame, text="Pemesanan Makanan: 0", font=("Merriweather", 12))
    label_meal.pack()
    
    def refresh_laporan():
        jumlah = len(data_pemesanan)
        total = hitung_total_pendapatan()
        rata = total / jumlah if jumlah > 0 else 0
        label_jumlah.config(text=f"Jumlah Pemesanan: {jumlah}")
        label_pendapatan.config(text=f"Total Pendapatan: Rp {total:,.0f}")
        label_rata_harga.config(text=f"Rata-rata Harga: Rp {rata:,.0f}")
        for kelas, label in zip(["Ekonomi", "Bisnis", "First Class"], [label_ekonomi, label_bisnis, label_first]):
            count = sum(1 for d in data_pemesanan if d['kelas'] == kelas)
            label.config(text=f"{kelas}: {count}")
        label_meal.config(text=f"Pemesanan Makanan: {sum(1 for d in data_pemesanan if d['meal'])}")
    tk.Button(frame, text="Refresh Laporan", width=15, command=refresh_laporan).pack()
    tk.Button(frame, text="Kembali", width=15, command=lambda: tampilkan_halaman("utama")).pack()
    refresh_laporan()
    return frame
  
frames = {"utama": buat_halaman_utama(), "input": buat_form_input(), "tampil": buat_tampil_data(), "cari": buat_pencarian_data(), "laporan": buat_hasil_laporan()}
tampilkan_halaman("utama")
root.mainloop()

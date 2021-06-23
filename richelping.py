from pathlib import Path
import json
import pickle

kmls = 'kmls'
kmls2 = 'kmls2'
tsim = {kmls: {}, kmls2: {}}

def stats(inpu = Path("./results"), name = None):
    global tsim
    donde = None
    for i in inpu.glob('*.json'):
        para = i.name[:-5].split('-')[1:6]
        donde = kmls if "norm" in para[4] else kmls2
        if donde == kmls:
            para[4] = para[4][:-5]
        dat = tuple(json.load(open(i, 'r')))
        if tuple(para[:-1]) not in tsim[donde][name].keys():
            tsim[donde][name][tuple(para[:-1])] = {}
        tsim[donde][name][tuple(para[:-1])][tuple(para[-1])]  = dat
    return    1 

def compare_intra_best_kmls2():
    file = open(Path("./results/analisis_intra.txt"), 'w')
    rmse_b = 10000000000
    psnr_b = 0
    snr_b = 10000000000
    cual_b = [0,0,0]
    for img in tsim[kmls2]:
#        file.write(f"Imagen {img}:\n")
        rmse_p = 100000000
        psnr_p = 0
        snr_p = 1000000000
        cual_p = [0,0,0]
        for p in tsim[kmls2][img]:
#            file.writelines(f"-- Parametros {p} :\n")
            rmse_it = 100000000
            psnr_it = 0
            snr_it = 1000000000
            cual_it = [0,0,0]
            for it in tsim[kmls2][img][p]:
                rmse, psnr, snr = tsim[kmls2][img][p][it]
                if rmse < rmse_it:
                    rmse_it = rmse
                    cual_it[0] = it
                if psnr > psnr_it:
                    psnr_it = psnr
                    cual_it[1] = it
                if snr < snr_it:
                    snr_it = snr
                    cual_it[2] = it
            file.write(f"---- Mejor Iteracion para Imagen {img} con parametros {p}:\n------ {cual_it}\n\n")
            if rmse_it < rmse_p:
                rmse_p = rmse_it
                cual_p[0] = p
            if psnr_it > psnr_p:
                psnr_p = psnr_it
                cual_p[1] = p
            if snr_it < snr_p:
                snr_p = snr_it
                cual_p[2] = p
        file.write(f"-- Mejor parametro para Imagen {img} :\n---- {cual_p}\n\n")
        if rmse_p < rmse_b:
            rmse_b = rmse_p
            cual_b[0] = img
        if psnr_p > psnr_b:
            psnr_b = psnr_b
            cual_b[1] = img
        if snr_p < snr_b:
            snr_b = snr_p
            cual_b[2] = img
    file.write(f"-- Mejor Imagen :\n---- {cual_b}\n\n")
#        file.write("\n\n")
    file.flush()
    file.close()
    return 1

def compare_intra_worst_kmls2():
    file = open(Path("./results/analisis_intra_worst.txt"), 'w')
    rmse_b = 0
    psnr_b = 100000000000
    snr_b = 0
    cual_b = [0,0,0]
    for img in tsim[kmls2]:
#        file.write(f"Imagen {img}:\n")
        rmse_p = 0
        psnr_p = 100000000
        snr_p = 0
        cual_p = [0,0,0]
        for p in tsim[kmls2][img]:
#            file.writelines(f"-- Parametros {p} :\n")
            rmse_it = 0
            psnr_it = 1000000000
            snr_it = 0
            cual_it = [0,0,0]
            for it in tsim[kmls2][img][p]:
                rmse, psnr, snr = tsim[kmls2][img][p][it]
                if rmse > rmse_it:
                    rmse_it = rmse
                    cual_it[0] = it
                if psnr < psnr_it:
                    psnr_it = psnr
                    cual_it[1] = it
                if snr > snr_it:
                    snr_it = snr
                    cual_it[2] = it
            file.write(f"---- Mejor Iteracion para Imagen {img} con parametros {p}:\n------ {cual_it}\n\n")
            if rmse_it > rmse_p:
                rmse_p = rmse_it
                cual_p[0] = p
            if psnr_it < psnr_p:
                psnr_p = psnr_it
                cual_p[1] = p
            if snr_it > snr_p:
                snr_p = snr_it
                cual_p[2] = p
        file.write(f"-- Mejor parametro para Imagen {img} :\n---- {cual_p}\n\n")
        if rmse_p > rmse_b:
            rmse_b = rmse_p
            cual_b[0] = img
        if psnr_p < psnr_b:
            psnr_b = psnr_b
            cual_b[1] = img
        if snr_p > snr_b:
            snr_b = snr_p
            cual_b[2] = img
    file.write(f"-- Mejor Imagen :\n---- {cual_b}\n\n")
#        file.write("\n\n")
    file.flush()
    file.close()
    return 1

  
    
#TIP DONE
def compare_kmlss():
    file = open(Path("./results/analisis_comparacion.txt"), 'w')
    for img in tsim[kmls]:
        file.write(f"Imagen {img}:\n")
        for p in tsim[kmls][img]:
            file.writelines(f"-- Parametros {p} :\n")
            for it in sorted(tsim[kmls][img][p]):
                file.write(f"---- Iteracion {it} : ")
                a = tsim[kmls][img][p][it][0]-tsim[kmls2][img][p][it][0]
                b = tsim[kmls2][img][p][it][1]-tsim[kmls][img][p][it][1]
                c = tsim[kmls][img][p][it][2]-tsim[kmls2][img][p][it][2]
                file.writelines(f"{(a,b,c)}\n")
        file.write("\n\n")
    file.flush()
    file.close()
    return 1

from pylab import imsave, gray
import numpy as np
def test_image_redrawing():
    dire = Path("./results/test.pickledge")
    dori = Path("./results/orig.pickled")
    print(dire)
    global img, ori, sol
    img = pickle.load(open(dire,"rb"))
    ori = pickle.load(open(dori,"rb"))
    gray()
    ma = max([max(i) for i in img])
    mao = max([max(i) for i in ori])
#    print(ma)
#    input("waiting")
    img *= (255/(ma+.01))
    ori *= (255/(mao+.01))
    sol = (img+ori)/2
    ma = max([max(i) for i in sol])
    sol *= (255/(ma+.01))
    imsave("./results/testsup.png", sol)
#    imsave("./results/test01.jpg", img)
#    img = np.array([[255 for j in range(len(img[0]))] for i in range(len(img)) ]) - img
#    imsave("./results/test00.jpg", img)

#test_image_redrawing()

def acomoda_snr(snr):
    
    return "{:.6f}".format(snr)

def create_tables_tesis():
    donde = None
    for val in [ x for x in dire.glob("*") if x.is_dir() ]:
#        print(val)
        file = open(Path("./results/"+val.name+".table"), "w")
        file.write(r"""\begin{table}
	\tbl{Results with parameters """)
        #TODO Que queden mejor los parametros
        upbd, upbf = val.name.split("-")
        file.write(f"$wep = {upbd}$, $sep = {upbf}$")
        file.write(r"""}
{
\begin{tabular}{||c||c|c|c||c|c|c||}
\hline
\hline 
Algorithm & \multicolumn{3}{c||}{KMLS} & \multicolumn{3}{c||}{KMLS2} \\ 
\hline 
Image & RMSE & PSNR & SNR & RMSE & PSNR & SNR \\  
\hline """)
        file.write("\n")
        for img in [ x for x in val.glob("*") if x.is_dir() ] :
            name = img.name[:img.name.find("_")][-4:]
            file.write(name+" ")
            datkmls = ["-", "-", "-"]
            datkmls2 = ["-", "-", "-"]
            n = 0
            for i in img.glob('*.json'):
#                print(i)
                para = i.name[:-5].split('-')[1:6]
                donde = kmls if "norm" in para[4] else kmls2
                if donde == kmls:
                    para[4] = para[4][:-5]  
                if para[-1] == "10":
                    #TIP Aqui es donde ejecutar las cosas
                    print(para)
                    n = int(para[3])
                    rmse, psnr, snr = tuple(json.load(open(i, 'r')))
                    if donde == kmls2:
                        datkmls2[0] = str(rmse)[:7]
                        datkmls2[1] = str(psnr)[:7]
                        datkmls2[2] = acomoda_snr(snr)
                        print(datkmls2)
                    else:
                        datkmls[0] = str(rmse)[:7]
                        datkmls[1] = str(psnr)[:7]
                        datkmls[2] = acomoda_snr(snr)
                        print(datkmls)
                    
            #TODO A este nivel va la creacion de la fila
            file.write(f" ({n}) &")
            file.write(f" {datkmls2[0]} & {datkmls2[1]} & {datkmls2[2]} & ")
            file.write(f" {datkmls[0]} & {datkmls[1]} & {datkmls[2]} ")
            file.write(r"""\\ 
\hline """)
            file.write("\n")
#            print("aqui")

        
        file.write(r"""\hline 
\end{tabular} }
    \label{tab:coef_""")
        file.write(f"{val.name} ")
        file.write(""" } """)
        file.write("\n")
        file.write(r"""\end{table}""")
        file.flush()
        file.close()
        #        tsim[donde][name][para][tuple(para[:4])][para[4]] = dat
#                if tuple(para[:-1]) not in tsim[donde][name].keys():
#                    tsim[donde][name][tuple(para[:-1])] = {}
#                tsim[donde][name][tuple(para[:-1])][tuple(para[-1])]  = dat

    return 1


if __name__ == "__main__":
    dire = Path("./results")
    for val in [ x for x in dire.glob("*") if x.is_dir() ]:
        for img in [ x for x in val.glob("*") if x.is_dir() ] :
            name = img.name[:img.name.find("_")]
            if name not in tsim[kmls].keys():
                tsim[kmls][name] = {}
                tsim[kmls2][name] = {}
#            print(f'===================\n Imagen {img}')
            stats(img, name)
#            print(f'===================\n\n\n ')
#    compare_intra_best_kmls2()
#    compare_intra_worst_kmls2()
#    compare_kmlss()
#    create_tables_tesis()
            








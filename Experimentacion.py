from time import clock, time
import sys
from random import randint

from Utils import parametros
import OpenImg as oim
from Main import apply_noise, to_process, process, Path

logs=Path('./output/logs')

o = 1
t = 10
h = 0.25 

n_clusters = [8, 9, 14, 16, 18, 23]

kwep=[0.5593, 0.6614, 0.4590, 0.2593, 0.1512]
ksep=[0.0652, 0.0179, 0.0889, 0.0351, 0.0012]

save_all = True

if __name__=="__main__":
    logger=open(logs/Path(f'{time()}.log'),'a')
    sys.stdout=logger
    oim.load_images()
    apply_noise(o)
    
    tiempo=0
    while not to_process.empty():
        a=to_process.get()
        for wep in kwep:
            for sep in ksep:
                for i in n_clusters:
                    print(f'{type(a)}\n  {a}\n')
                    param=parametros(t, wep, sep, i, h, randint(2000, 1000000), save_all)
                    print(f'Usando parametros: {param}\n')
                    time=clock()
                    process(param , a, False)
                    time=clock()-time
                    print(f'\nTiempo total de {a}: {time}\n')
                    tiempo+=time
        
    print(f'\n\n\nTiempo total {tiempo}\n')
    sys.stdout=sys.__stdout__
    logger.close()
    print('I finish')

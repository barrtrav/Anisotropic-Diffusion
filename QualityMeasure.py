from pylab import log10, inf, mean

def RMSE(img_org, img_res):
    rmse = 0
    m = img_org.shape[0]
    n = img_org.shape[1]
    for x in range(0, img_org.shape[0]):
        for y in range(0, img_org.shape[1]):
             rmse += (img_org[x, y] - img_res[x, y])**2

    return rmse/(m*n)

def PSNR(img_org, img_res, rmse):
    max_pix = -inf
    for i in range(0, img_org.shape[0]):
        m = max(img_res[1])
        if m > max_pix:
            max_pix = m
    max_pix = max_pix**2
    psnr = 10*log10(max_pix/rmse)
    return psnr

def quality_measures(img_org, img_res):
    """Returns a tuple with RMSE, PSNR, and SNR"""
    rmse = float(0)
    max_pix = -inf
    mean_pixR = mean(img_res)
    mean_pixO = mean(img_org)
    standar_der = int(0)
    psnr=inf
    m = img_org.shape[0]
    n = img_org.shape[1]

    for x in range(0, m):
        for y in range(0, n):
            pixO = img_org[x, y]
            pixR = img_res[x, y]

            rmse += (float(pixO) - float(pixR))**2

            if pixR > max_pix:
                max_pix = pixR

            standar_der += (float(mean_pixO) - float(pixO))**2

    rmse /= (m*n)#hasta aqui es MSE
    max_pix = (float(max_pix))**2
    if rmse!=0:
        psnr = 10*log10(max_pix/rmse)
        
    rmse=rmse**0.5
    standar_der = (standar_der)**0.5
    snr = mean_pixR/standar_der

    return (rmse, psnr, snr)


import _libspheroid as lsd
import numpy as np

__ALL__=['SpheroidCalc','lsd']

class SpheroidCalc(object):
    def __init__(self, input_fname):
        self.input_fname = input_fname
        # читаем файл с настройками
        lsd.dls_read_input(input_fname)
        # выделяем памят для хранения промежуточных массивов
        lsd.alloc_dls_array(lsd.mo_dls.key,
                            lsd.mo_dls.keyel, 1)
    def finalize(self):
        lsd.alloc_dls_array(lsd.mo_dls.key,
                            lsd.mo_dls.keyel, 2)
    
    def set_refr_index(self, m):
        lsd.mo_dls.rn.flat[0] = m.real
        lsd.mo_dls.rk.flat[0] = m.imag
    
    def get_refr_index(self):
        m = complex(lsd.mo_dls.rn.flat[0], lsd.mo_dls.rk.flat[0])
        return m
    
    def set_wvl(self, wvl):
        lsd.mo_dls.wl = wvl
    
    def get_wvl(self):
        wvl = float(lsd.mo_dls.wl)
        return wvl
    
    def get_knots_count(self):
        return int(lsd.mo_dls.kn)
    
    def set_knots_count(self, knots_count):
        lsd.mo_dls.kn = knots_count
    
    def set_radii(self, rr):
        kn = len(rr)
        self.knots_count = kn
        lsd.mo_dls.grid[:kn] = rr[:]
        
    def set_sd(self, sd):
        kn = len(sd)
        if kn!= self.knots_count:
            raise Exception("Invalid SD len")
        
        lsd.mo_dls.sd[:kn] = sd[:]
        
    def get_radii(self):
        return lsd.mo_dls.grid[:self.knots_count]
    
    def get_sd(self):
        return lsd.mo_dls.sd[:self.knots_count]
    
    def set_psd(self, psd):
        try:
            rr, SD = psd
        except ValueError:
            raise ValueError("Pass an iterable with two items")
        else:
            self.radii = rr
            self.sd = SD
    
    def get_psd(self):
        return self.radii, self.sd
    
    def calc(self):
        lsd.optchar(lsd.mo_dls.ndp)
    
    def get_ext(self):
        return float(lsd.mo_dls.xext)
    
    def get_sca(self):
        return float(lsd.mo_dls.xsca)
    
    def get_abs(self):
        return float(lsd.mo_dls.xabs)
    
    def get_lbr(self):
        return float(lsd.mo_dls.xblr)
    
    def get_ldr(self):
        return float(lsd.mo_dls.xldr)

    def get_angle(self):
        self.km = int(lsd.mo_dls.km)        
        return lsd.mo_dls.angle[:self.km]

    def get_angle_rad(self):
        return self.get_angle()*3.14159265/180.0

    def get_f11(self):
        self.km = int(lsd.mo_dls.km)
        return lsd.mo_dls.f11[:self.km]

    def get_f12(self):
        self.km = int(lsd.mo_dls.km)
        return -lsd.mo_dls.f12[:self.km]

    def get_f22(self):
        self.km = int(lsd.mo_dls.km)
        return lsd.mo_dls.f22[:self.km]

    def get_f33(self):
        self.km = int(lsd.mo_dls.km)
        return lsd.mo_dls.f33[:self.km]

    def get_f34(self):
        self.km = int(lsd.mo_dls.km)
        return lsd.mo_dls.f34[:self.km]

    def get_f44(self):
        self.km = int(lsd.mo_dls.km)
        return lsd.mo_dls.f44[:self.km]

    def get_matr(self):
        self.km = int(lsd.mo_dls.km)
        f11 = self.get_f11()
        matr = np.c_[f11, self.get_f12()*f11, self.get_f22()*f11,
                     self.get_f33()*f11, self.get_f34()*f11,
                     self.get_f44()*f11]
        return matr
        
    def get_full_matr(self):
        self.km = int(lsd.mo_dls.km)
        f11 = self.get_f11()
        matr = np.zeros((self.km, 16), dtype='float')
        matr[:,0] = f11
        matr[:,1] = self.get_f12()*f11
        matr[:,4] = matr[:,1]
        matr[:,5] = self.get_f22()*f11
        matr[:,10] = self.get_f33()*f11
        matr[:,11] = self.get_f34()*f11
        matr[:,14] = -matr[:,11]
        matr[:,15] = self.get_f44()*f11
        return matr

    def get_Ageom(self):
        r = self.get_radii()
        dlnr = np.log(r[1]/r[0])
        dvdlnr = self.get_sd()
        dsdlnr = 3*dvdlnr/(4*r)
        S0 = np.sum(dsdlnr)*dlnr
        GA = np.pi*self.get_ext()/(self.get_lbr()*S0)
        return GA
        
    def get_VolC(self):
        r = self.get_radii()
        dlnr = np.log(r[1]/r[0])
        dvdlnr = self.get_sd()
        
        V0 = np.sum(dvdlnr)*dlnr
        return V0
    
    psd = property(get_psd, set_psd)
    radii = property(get_radii, set_radii)
    sd = property(get_sd, set_sd)
    midx = property(get_refr_index, set_refr_index)
    wvl  = property(get_wvl, set_wvl)
    knots_count = property(get_knots_count, set_knots_count)
    ext = property(get_ext)
    sca = property(get_sca)
    absb = property(get_abs)
    lbr = property(get_lbr)
    ldr = property(get_ldr)
    angle = property(get_angle)
    F11 = property(get_f11)
    F12 = property(get_f12)
    F22 = property(get_f22)
    F33 = property(get_f33)
    F34 = property(get_f34)
    F44 = property(get_f44)
    MTX = property(get_matr)
    FMTX = property(get_full_matr)
    VolC = property(get_VolC)
    GAlb= property(get_Ageom)

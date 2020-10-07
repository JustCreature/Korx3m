import math

class Model_Korx:

    @staticmethod
    def korx_math_model(Dp_f, Lvh_f, L12_f, Lvih_f, Lk_f, Lm_f, a11_f, a12_f,
                        a2_f, fee_f, beta_f, Lsm_f, L2_f, gamma1_f, gamma2_f,
                        Dopr_f, Lopr_f, Dz_f, Lz_f, Kz_f, Dg_f, Sg_f, A_f, En_f,
                        ksi_f="None", c_f="None", b_f="None", screws=[], Xa=0, c_check=0, En_check=0,
                        temp_koeff=1.013, Lcu_f=20):

        result = {
            'a': 1,
            'b': 1,
            'c': 1,
            'Ep': 1,
            'ksi': 1,
            'En': 1,
            'Lr': 1,
            'mu': 1,
            'GF': 1,
            'Dvh': 1,
            'Dvih': 1,
            'L': 1,
            'X1': 1,
            'X2': 1,
            'Lod': 1,
            'err': 1,
            'warn': 1,

            "Dg": 1,
            "dg": 1,
            "use_ksi": 0 if ksi_f == "None" else 1,
            "use_c": 0 if c_f == "None" else 1,
            "use_b": 0 if b_f == "None" else 1,
            "Sg": 1,

            "IO1": 1,
            "IO2": 1,
            "Lrab": 1,
        }



        return result




def main(n):
    Dp = 1200 #ininp
    Lvh = 485 #ininp
    L12 = 160 #ininp
    Lvih = 555 #ininp
    Lk = 0 #ininp
    Lm = 30 #ininp
    a11 = 2 #ininp
    a12 = 3.5 #ininp
    a2 = 2.5 #ininp
    fee = 0 #ininp
    beta = 10 #ininp
    Lsm = -30 #ininp
    L2 = 450 #ininp
    gamma1 = 3.5 #ininp
    gamma2 = 3 #ininp
    Dopr = 263 #ininp
    Lopr = 520 #ininp
    Dz = 340 #ininp
    Lz = 5100 #ininp
    Kz = 3 #ininp
    Dg = 344 #ininp
    Sg = 32 #ininp
    A = 301 #ininp
    En = "No"





if __name__ == '__main__':
    main(1)
    main(2)
    main(3)


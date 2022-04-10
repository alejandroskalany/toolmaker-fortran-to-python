# ==============================================================================
# module : ToolDescUtil
# author : peter swinburne
# date   : 09/26/2021
# brief  : Tool Description Utility
# Note   : converted from M. Luling Fortran code
# ==============================================================================
# Title Comments from original Fortran Code
#   Program ToolDescriptionMaker generates a tool-description file for all the
#   axisymmetric LWD propagation-resistivity array tools.
#   A future version will address other tool classes as well.
#       1.0 written by Martin G. Luling, Paris, 18 April 2021.
#   Version 1.1 replaces the separate phase-shift and attenuation output modes
#   by a single, complex-valued output mode.
#       1.1 written by Martin G. Luling, Paris,  4 May 2021.
#   Version 1.2 corrects the default recess and coil diameters, which previously
#   were chosen at only half of their correct value.
#       1.2 written by Martin G. Luling, Paris, 18 May 2021.
# ==============================================================================

# define integer parameters
NTMAX = 10
NRMAX = 3
NFMAX = 5
NMMAX = 20
NOMAX = 50

# define string parameters
FILOUT = ""
HEADER1 = ""
HEADER2 = ""
LSCALE = ""
YN = ""

# define float point array parameters
ZT = [0.0] * NTMAX
R1T = [0.0] * NTMAX
R2T = [0.0] * NTMAX
R3T = [0.0] * NTMAX

ZR = [0.0] * NRMAX
R1R = [0.0] * NRMAX
R2R = [0.0] * NRMAX
R3R = [0.0] * NRMAX

FREQ = [0.0] * NFMAX
EPS = [[0.0] * 3] * NFMAX
BHC = [[0.0] * 3] * NFMAX

# there was a declaration error for MM and MBHC (PS)
MM = [[0] * NMMAX] * 10
MBHC = [[0] * (NMMAX + 1)] * 10
NTT = [0] * NTMAX
NTR = [0] * NRMAX

# @@@I = 0
# @@@it = 0
J = 0
JR = 0
KF = 0
LM = 0
MO = 0
# @@@NT = 0
# @@@NR = 0
# @@@NF = 0
NM = 0
NO = 0

CR = '\n'


# ==============================================================================
def tool_description():
    """
    :param: none
    :return: none
    """
    global R1T, R2T, R3T
    global R1R, R2R, R3R

    # Read the file-header information
    header1 = input('Enter the name of the service company: ') or 'SLB'
    print(header1)
    header2 = input('Enter the tool name and size, such as ''ARC825'': ') or 'ARC825'
    print(header2)

    # Prepare and open the sonde-description output file and write the header lines in there
    sonde_filename = header2 + '.sde'
    sonde_file = open(sonde_filename, 'wt')
    header_str = header1 + ' ' + header2 + '\n'
    sonde_file.write(header_str)
    sonde_file.write('Sonde description from 2016 SPWLA catalogue by No-Hidden-Pay 2021.\n')

    # Enter length scale and other global tool information:
    lscale = input('Choose your length scale (in - cm - mm): ') or 'in'
    print(lscale)

    sonde_file.write(lscale)
    sonde_file.write(CR)

    yn = input('Are all transmitter and receiver antennas identical? <YN> : ') or 'Y'
    print(yn)
    yn = yn.lower()
    if yn == 'y':
        print('Enter the antenna-recess diameter,')
        print('The coil diameter,')
        print('The collar diameter')
        print('Enter 0.0 for unknown antenna recess and coil diameters): ')
        R1T[0] = input('Antenna-recess diameter: ') or '0.0'
        print(R1T[0])
        R2T[0] = input('The Coil Diameter: ') or '0'
        print(R2T[0])
        R3T[0] = input('The Collar Diameter: ') or '8.25'
        print(R3T[0])
        if R1T[0] == 0.0:
            R1T[0] = R3T[0] - 0.5
        if R2T[0] == 0.0:
            R2T[0] = R3T[0] - 0.2

        NTT[0] = input('Enter the number of antenna-coil windings (enter 0.0, if not known: ') or '8'
        if NTT[0] == 0.0:
            NTT[0] = 10
        print(NTT[0])

    nt = input('How many transmitters does your tool have?: ') or '5'
    int_nt = int(nt)
    print(int_nt)

    #   Read all transmitter information:
    print("Enter these next values...")
    for it in range(0, int_nt):
        istr = input('For transmitter ' + str(it + 1) + ' enter the axial position: ')
        ZT[it] = float(istr)
        if yn == 'y':
            R1T[it] = R1T[0]
            R2T[it] = R2T[0]
            R3T[it] = R3T[0]
            NTT[it] = NTT[0]
        else:
            print('Enter the antenna-recess diameter,')
            print('The coil diameter,')
            print('The collar diameter')
            print('Enter 0.0 for unknown antenna recess and coil diameters): ')
            R1T[it] = input('Antenna-recess diameter: ') or '0.0'
            print(R1T[it])
            R2T[it] = input('The Coil Diameter: ') or '0.0'
            print(R2T[it])
            R3T[it] = input('The Collar Diameter: ') or '8.25'
            print(R3T[it])
            if R1T[it] == 0.0:
                R1T[it] = R3T[it] - 0.5
            if R2T[it] == 0.0:
                R2T[it] = R3T[it] - 0.2
            NTT[it] = input('Enter the number of antenna-coil windings (enter 0, if not known): ') or '8'
            print(NTT[it])
            if NTT[it] == 0.0:
                NTT[it] = 10

    nr = input('How many receivers does your tool have?: ') or '2'
    int_nr = int(nr)
    print(int_nr)

    #   Read all receiver information:
    print('Enter these next values...')
    for it in range(0, int_nr):
        jstr = input('For receiver ' + str(it + 1) + ' enter the axial position: ')
        ZR[it] = float(jstr)
        if yn == 'y':
            R1R[it] = R1R[0]
            R2R[it] = R2R[0]
            R3R[it] = R3R[0]
            NTR[it] = NTR[0]
        else:
            print('Enter the antenna-recess diameter,')
            print('The coil diameter,')
            print('The collar diameter')
            print('Enter 0.0 for unknown antenna recess and coil diameters): ')
            R1R[it] = input('Antenna-recess diameter: ')
            R2R[it] = input('The Coil Diameter: ')
            R3R[it] = input('The Collar Diameter: ')
            if R1R[it] == 0.0:
                R1R[it] = R3R[it] - 0.5
            if R2R[it] == 0.0:
                R2R[it] = R3R[it] - 0.2
            NTR[it] = input('Enter the number of antenna-coil windings (enter 0, if not known: ')    # str6
            if NTR[it] == 0.0:
                NTR[it] = 10

    # Read all operating frequencies:
    nf = input('How many operating frequencies does your tool have? :') or '2'
    int_nf = int(nf)
    print(int_nf)

    print('You must Enter these next values..')
    for kf in range(0, int_nf):
        FREQ[kf] = input('Enter the operating frequency ' + str(kf + 1) + ' in kHz): ')
        EPS[kf][0] = input('Enter the dielectric-estimate coefficient 1 :')
        EPS[kf][1] = input('Enter the dielectric-estimate coefficient 2 :')
        EPS[kf][2] = input('Enter the dielectric-estimate coefficient 3 :')

    # Read the single-transmitter - single-frequency raw-measurement modes:
    if int_nr == 2:
        int_nm = int_nt * int_nf
        print('single-transmitter, raw-measurement modes, Indices for mode, T, R1, R2, Freq, Mode    T   R1   R2 Freq:')    # str21

        for kf in range(0, int_nf):
            for it in range(0, int_nt):
                q = it + (int_nt * kf)
                # @@@print(q)
                MM[q][0] = it
                if ZT[it] > 0.0:
                    MM[it + (int_nt * kf)][1] = 1
                    MM[it + (int_nt * kf)][2] = 2
                else:
                    MM[it + (int_nt * kf)][1] = 2
                    MM[it + (int_nt * kf)][2] = 1

                MM[it + (int_nt * kf)][3] = kf + 1
                print(it + (int_nt * kf) + 1, MM[it + (int_nt * kf)][0] + 1, MM[it + (int_nt * kf)][1], MM[it + (int_nt * kf)][2], MM[it + (int_nt * kf)][3])
    else:
        nm = input('How many single-transmitter-measurement modes does the tool have? :')    # str23
        int_nm = int(nm)

        for lm in range(0, int_nm):
            print('For measurement mode ' + str(lm))
            istr = input('Enter the transmitter index :')
            MM[lm][0] = int(istr)
            istr = input('Enter the near receiver index :')
            MM[lm][1] = int(istr)
            istr = input('Enter the far receiver index : ')
            MM[lm][2] = int(istr)
            istr = input('Enter the frequency index:')
            MM[lm][3] = int(istr)

    # Read the borehole-compensated output modes:
    istr = input('How many borehole-compensated output modes does the tool have? :') or ' 10'
    int_no = int(istr)
    print(int_no)

    for mo in range(0, int_no):
        psch = input('Enter the name of the phase-shift channel for output mode ' + str(mo + 1) + ' (maximal eight characters):')
        atch = input('Enter the name of the attenuation channel for output mode ' + str(mo + 1) + ' (maximal eight characters):')
        # @@@mo[0] = str(psch)
        # @@@mo[1] = str(atch)
        mstr = input('Output mode ' + str(mo + 1) + ' combines how many single-transmitter modes? :')
        MBHC[0][mo] = int(mstr)
        for lm in range(0, MBHC[0][mo]):
            print('For output mode ' + str(mo + 1) + ' : ' + str(lm + 1))
            istr = input('Enter the index of single-transmitter mode : ')
            MBHC[lm + 1][mo] = int(istr)
            istr = input('Enter the borehole-compensation weight: ')
            BHC[lm][mo] = float(istr)  # @@@ index out of range

    # Write the collected tool-description data to the output file:
    dstr = str(int_nt) + ', ' + str(int_nr) + ', ' + str(int_nf) + ', ' + str(int_nm) + ', ' + str(int_no)
    sonde_file.write(dstr)
    for it in range(0, int_nt):
        dstr = str(it) + ', ' + str(ZT[it]) + ', ' + str(R1T[it]) + ', ' + str(R2T[it]) + ', ' + str(R3T[it]) + ', ' + str(NTT[it])
        sonde_file.write(dstr)

    for jr in range(0, int_nr):
        dstr = str(jr) + ', ' + str(ZR[jr]) + ', ' + str(R1R[jr]) + ', ' + str(R2R[jr]) + ', ' + str(R3R[jr]) + ', ' + str(NTR[jr])
        sonde_file.write(dstr)

    for kf in range(0, int_nf):
        dstr = str(kf) + ', ' + str(FREQ[kf]) + ', ' + str(EPS[kf][0]) + ', ' + str(EPS[kf][1]) + ', ' + str(EPS[kf][2])
        sonde_file.write(dstr)

    for lm in range(0, int_nm):
        dstr = str(lm) + ', ' + str(MM[lm][0]) + ', ' + str(MM[lm][1]) + ', ' + str(MM[lm][2]) + ', ' + str(MM[lm][3])
        sonde_file.write(dstr)

    for mo in range(0, int_no):
        dstr = str(mo) + ', ' + str(MBHC[0][mo]) + 'PS + iAT'
        sonde_file.write(dstr)

        dstr = str(MBHC[1][mo]) + ', ' + str(BHC[0][mo]) + ', ' + str(MBHC[0][mo])
        sonde_file.write(dstr)

    print('That''s all, folks!')

    sonde_file.close()

    return


# ============================================================
if __name__ == '__main__':
    # call the function
    tool_description()

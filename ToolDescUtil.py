# ==============================================================================
# module : ToolDescUtil
# author : peter swinburne
# date   : 09/26/2021 - 4/10/2022
# brief  : Tool Description Utility (sonde)
# Note   : converted from M. Luling Fortran code
# version: 2.0
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

# define float point array parameters
zt = [0.0 for i in range(NTMAX)]
r1t = [0.0 for i in range(NTMAX)]
r2t = [0.0 for i in range(NTMAX)]
r3t = [0.0 for i in range(NTMAX)]

zr = [0.0 for i in range(NRMAX)]
r1r = [0.0 for i in range(NRMAX)]
r2r = [0.0 for i in range(NRMAX)]
r3r = [0.0 for i in range(NRMAX)]

freq = [0.0] * NFMAX
eps = [[0.0 for i in range(NTMAX)] for j in range(NFMAX)]
bhc = [[0.0 for i in range(NTMAX)] for j in range(NFMAX)]

mm = [[0 for i in range(NMMAX)] for j in range(NTMAX)]
mbhc = [[0 for i in range(NMMAX + 1)] for j in range(NTMAX * NRMAX)]
ntt = [0 for i in range(NTMAX)]
ntr = [0 for i in range(NRMAX)]
chan_name = [[' ' for i in range(2)] for j in range(NMMAX)]

NO_EXECUTE = 0


# ==============================================================================
def tool_description():
    """
    :param: none
    :return: none
    """
    global zt, r1t, r2t, r3t, zr, r1r, r2r, r3r
    global freq, eps, bhc

    # string float format
    pt = -5.056789
    pit = 10
    s = str("{: 3.3f}".format(pt))
    s += str("{:5}".format(pit))
    print(s)
    pt = 5.056789
    pit = 100
    s = str("{: 3.3f}".format(pt))
    s += str("{:5}".format(pit))
    print(s)
    chan_name[2][0] = 'PS16L'
    chan_name[2][1] = 'AT16L'
    print(chan_name)

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
    sonde_file.write('\n')

    yn = input('Are all transmitter and receiver antennas identical? <YN> : ') or 'Y'
    yn = yn.lower()
    print(yn)
    if yn == 'y':
        print('Enter the antenna-recess diameter,')
        print('The coil diameter,')
        print('The collar diameter')
        print('Enter 0.0 for unknown antenna recess and coil diameters): ')
        fstr = input('Antenna-recess diameter: ') or 0.0
        r1t[0] = float(fstr)
        print(r1t[0])
        fstr = input('The Coil Diameter: ') or 0.0
        r2t[0] = float(fstr)
        print(r2t[0])
        fstr = input('The Collar Diameter: ') or 8.25
        r3t[0] = float(fstr)
        print(r3t[0])
        if r1t[0] == 0.0:
            r1t[0] = r3t[0] - 0.5
        if r2t[0] == 0.0:
            r2t[0] = r3t[0] - 0.2

        fstr = input('Enter the number of antenna-coil windings (enter 0.0, if not known: ') or 8.0
        ntt[0] = int(fstr)
        if ntt[0] == 0.0:
            ntt[0] = 10
        print(ntt[0])

    istr = input('How many transmitters does your tool have?: ') or 5
    int_nt = int(istr)
    print(int_nt)

    #   Read all transmitter information:
    print("Enter these next values...")
    for it in range(0, int_nt):
        fstr = input('For transmitter ' + str(it + 1) + ' enter the axial position: ')
        zt[it] = float(fstr)
        if yn == 'y':
            r1t[it] = r1t[0]
            r2t[it] = r2t[0]
            r3t[it] = r3t[0]
            ntt[it] = ntt[0]
        else:
            print('Enter the antenna-recess diameter,')
            print('The coil diameter,')
            print('The collar diameter')
            print('Enter 0.0 for unknown antenna recess and coil diameters): ')
            fstr = input('Antenna-recess diameter: ') or 0.0
            r1t[it] = float(fstr)
            print(r1t[it])
            fstr = input('The Coil Diameter: ') or 0.0
            r2t[it] = float(fstr)
            print(r2t[it])
            fstr = input('The Collar Diameter: ') or 8.25
            r3t[it] = float(fstr)
            print(r3t[it])
            if r1t[it] == 0.0:
                r1t[it] = r3t[it] - 0.5
            if r2t[it] == 0.0:
                r2t[it] = r3t[it] - 0.2
            istr = input('Enter the number of antenna-coil windings (enter 0, if not known): ') or 8
            ntt[it] = int(istr)
            print(ntt[it])
            if ntt[it] == 0.0:
                ntt[it] = 10

    nr = input('How many receivers does your tool have?: ') or 2
    int_nr = int(nr)
    print(int_nr)

    #   Read all receiver information:
    print('Enter these next values...')
    for it in range(0, int_nr):
        jstr = input('For receiver ' + str(it + 1) + ' enter the axial position: ')
        zr[it] = float(jstr)
        if yn == 'y':
            r1r[it] = r1t[0]
            r2r[it] = r2t[0]
            r3r[it] = r3t[0]
            ntr[it] = ntt[0]
        else:
            print('Enter the antenna-recess diameter,')
            print('The coil diameter,')
            print('The collar diameter')
            print('Enter 0.0 for unknown antenna recess and coil diameters): ')
            fstr = input('Antenna-recess diameter: ')
            r1r[it] = float(fstr)
            fstr = input('The Coil Diameter: ')
            r2r[it] = float(fstr)
            fstr = input('The Collar Diameter: ')
            r3r[it] = float(fstr)
            if r1r[it] == 0.0:
                r1r[it] = r3r[it] - 0.5
            if r2r[it] == 0.0:
                r2r[it] = r3r[it] - 0.2
            istr = input('Enter the number of antenna-coil windings (enter 0, if not known: ')
            ntr[it] = int(istr)
            if ntr[it] == 0.0:
                ntr[it] = 10

    # Read all operating frequencies:
    istr = input('How many operating frequencies does your tool have? :') or 2
    int_nf = int(istr)
    print(int_nf)

    print('You must Enter these next values..')
    for kf in range(0, int_nf):
        fstr = input('Enter the operating frequency ' + str(kf + 1) + ' in kHz): ')
        freq[kf] = float(fstr)
        fstr = input('Enter the dielectric-estimate coefficient 1 :')
        eps[kf][0] = float(fstr)
        fstr = input('Enter the dielectric-estimate coefficient 2 :')
        eps[kf][1] = float(fstr)
        fstr = input('Enter the dielectric-estimate coefficient 3 :')
        eps[kf][2] = float(fstr)

    print(eps)

    # Read the single-transmitter - single-frequency raw-measurement modes:
    if int_nr == 2:
        int_nm = int_nt * int_nf
        print('single-transmitter, raw-measurement modes, Indices for mode, T, R1, R2, Freq, Mode    T   R1   R2 Freq:')

        for kf in range(0, int_nf):
            for it in range(0, int_nt):
                q = it + (int_nt * kf)
                # @@@print(q)
                mm[q][0] = it
                if zt[it] > 0.0:
                    mm[it + (int_nt * kf)][1] = 1
                    mm[it + (int_nt * kf)][2] = 2
                else:
                    mm[it + (int_nt * kf)][1] = 2
                    mm[it + (int_nt * kf)][2] = 1

                mm[it + (int_nt * kf)][3] = kf + 1
    else:
        nm = input('How many single-transmitter-measurement modes does the tool have? :')    # str23
        int_nm = int(nm)

        for lm in range(0, int_nm):
            print('For measurement mode ' + str(lm))
            istr = input('Enter the transmitter index :')
            mm[lm][0] = int(istr)
            istr = input('Enter the near receiver index :')
            mm[lm][1] = int(istr)
            istr = input('Enter the far receiver index : ')
            mm[lm][2] = int(istr)
            istr = input('Enter the frequency index:')
            mm[lm][3] = int(istr)

    # Read the borehole-compensated output modes:
    istr = input('How many borehole-compensated output modes does the tool have? :') or 10
    int_no = int(istr)
    print(int_no)

    # =============================================================
    # Write the collected tool-description data to the output file
    dstr = '      ' + str(int_nt) + ', ' \
                    + str(int_nr) + ', ' \
                    + str(int_nf) + ', ' \
                    + str(int_nm) + ', ' \
                    + str(int_no) + '\n'
    sonde_file.write(dstr)
    for it in range(0, int_nt):
        dstr = '  ' + str("{:3}".format(it + 1)) + ', ' \
               + str("{: 4.3f}".format(zt[it])) + ', ' \
               + str("{: 4.3f}".format(r1t[it])) + ', ' \
               + str("{: 4.3f}".format(r2t[it])) + ', ' \
               + str("{: 4.3f}".format(r3t[it])) + ', ' \
               + str("{:3}".format(ntt[it])) + ', ' \
               + '\n'
        sonde_file.write(dstr)

    for jr in range(0, int_nr):
        dstr = '  ' + str("{:3}".format(jr + 1)) + ', ' \
                    + str("{: 4.4f}".format(zr[jr])) + ', ' \
                    + str("{: 4.3f}".format(r1r[jr])) + ', ' \
                    + str("{: 4.3f}".format(r2r[jr])) + ', ' \
                    + str("{: 4.3f}".format(r3r[jr])) + ', ' \
                    + str("{:3}".format(ntr[jr])) + ', ' \
                    + '\n'
        sonde_file.write(dstr)

    for kf in range(0, int_nf):
        dstr = '  ' + str("{:3}".format(kf + 1)) + ', ' \
                    + str("{: 5.2f}".format(float(freq[kf]))) + ', ' \
                    + str("{: 4.2f}".format(float(eps[kf][0]))) + ', ' \
                    + str("{: 4.2f}".format(float(eps[kf][1]))) + ', ' \
                    + str("{: 4.2f}".format(float(eps[kf][2]))) + ', ' \
                    + '\n'
        sonde_file.write(dstr)

    for lm in range(0, int_nm):
        dstr = '  ' + str("{:3}".format(lm + 1)) + ', ' \
                    + str("{:3}".format(mm[lm][0] + 1)) + ', ' \
                    + str("{:3}".format(mm[lm][1])) + ', ' \
                    + str("{:3}".format(mm[lm][2])) + ', ' \
                    + str("{:3}".format(mm[lm][3])) + ', ' \
                    + '\n'
        sonde_file.write(dstr)

    for mo in range(0, int_no):
        psch = input('Enter name of phase-shift channel for output mode ' + str(mo + 1) + ' (max 8 characters):')
        atch = input('Enter name of attenuation channel for output mode ' + str(mo + 1) + ' (max 8 characters):')
        chan_name[mo][0] = str(psch)
        chan_name[mo][1] = str(atch)
        mstr = input('Output mode ' + str(mo + 1) + ' combines how many single-transmitter modes? :')
        mbhc[0][mo] = int(mstr)
        dstr = '    ' + str(mo + 1) + ', ' \
                      + str(mbhc[0][mo]) + ', ' \
                      + chan_name[mo][0] + ', ' \
                      + chan_name[mo][1] \
                      + '\n'
        sonde_file.write(dstr)

    if NO_EXECUTE:
        for lm in range(0, mbhc[0][mo]):
            print('For output mode ' + str(mo + 1) + ' : ' + str(lm + 1))
            istr = input('Enter the index of single-transmitter mode : ')
            mbhc[lm + 1][mo] = int(istr)
            istr = input('Enter the borehole-compensation weight: ')
            bhc[lm][mo] = float(istr)


        dstr = str(mbhc[1][mo]) + ', ' + str(bhc[0][mo]) + ', ' + str(mbhc[0][mo]) + '\n'
        sonde_file.write(dstr)

    sonde_file.close()

    print('Complete without error\n')

    return


# ============================================================
if __name__ == '__main__':
    # call the function
    tool_description()

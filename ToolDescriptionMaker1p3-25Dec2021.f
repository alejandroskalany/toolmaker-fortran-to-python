C   Program ToolDescriptionMaker generates a tool-description file for all the 
C   axisymmetric LWD propagation-resistivity array tools. 
C
C   A future version will address other tool classes as well. 
C   1.0 written by Martin G. Luling, Paris, 18 April 2021. 
C
C   Version 1.1 replaces the separate phase-shift and attenuation output modes 
C   by a single, complex-valued output mode. 
C   1.1 written by Martin G. Luling, Paris,  4 May 2021. 
C
C   Version 1.2 corrects the default recess and coil diameters, which previously
C   were chose at only half of their correct value. 
C   1.2 written by Martin G. Luling, Paris, 18 May 2021. 
C
C   Version 1.3 adds the names of the output modes to be user-entered. These 
C   output-mode names will be entered as headers to the processed-log files. 
C   1.3 written by Martin G. Luling, Paris, 25 December 2021. 
C
C   Copyright © 2021 by Martin G. Luling, all rights reserved. 
C
      PROGRAM TOOLDESCRIPTIONMAKER
      IMPLICIT NONE
C
      INTEGER NTMAX,NRMAX,NFMAX,NMMAX,NOMAX
      PARAMETER (NTMAX=10,NRMAX=3,NFMAX=3,NMMAX=20,NOMAX=50)
C
      CHARACTER *80 FILOUT,HEADER1,HEADER2
      CHARACTER *59 COPYRIGHT
      CHARACTER *10 NAME(NOMAX),NAMEPS,NAMEAT
      CHARACTER *2 LSCALE
      CHARACTER *1 YN
      REAL *8 ZT(NTMAX),R1T(NTMAX),R2T(NTMAX),R3T(NTMAX)
      REAL *8 ZR(NRMAX),R1R(NRMAX),R2R(NRMAX),R3R(NRMAX)
      REAL *8 FREQ(NFMAX),EPS(NFMAX,3),BHC(NMMAX,NOMAX)
      INTEGER MM(NMMAX,4),MBHC((NMMAX+1),NOMAX),NTT(NTMAX),NTR(NRMAX)
      INTEGER I,IT,J,JR,KF,LM,MO,NT,NR,NF,NM,NO
C
      COPYRIGHT='Copyright © 2021 by Martin G. Luling, all rights reserv
     1ed. '
C
    1 FORMAT ('Enter the name of the service company:')
    2 FORMAT ('Enter the tool name and size, such as ''ARC825'':')
    3 FORMAT ('Choose your length scale (in - cm - mm):')
    4 FORMAT ('Are all transmitter and receiver antennas identical? <YN>
     1')
    5 FORMAT ('Enter the antenna-recess diameter, the coil diameter and 
     1the collar diameter:',/,'Enter 0.0 for unknown antenna recess and 
     2coil diameters.')
    6 FORMAT ('Enter the number of antenna-coil windings (enter 0, if no
     1t known):')
   11 FORMAT ('How many transmitters does your tool have?')
   12 FORMAT ('For transmitter',I2,', enter the axial position:')
   13 FORMAT ('How many receivers does your tool have?')
   14 FORMAT ('For receiver',I2,', enter the axial position:')
   15 FORMAT ('How many operating frequencies does your tool have?')
   16 FORMAT ('Enter the operating frequency',I2,' (in kHz)',/,10X,'and 
     1the three dielectric-estimate coefficients:')
   22 FORMAT (5I5)
   23 FORMAT ('How many single-transmitter-measurement modes does the to
     1ol have?')
   24 FORMAT ('For measurement mode',I3,', enter the transmitter index,'
     1,/,31X,'the near and far receiver indices',/,31X,'and the frequenc
     2y index:')
   25 FORMAT ('How many borehole-compensated output modes does the tool 
     1have?')
   26 FORMAT ('Enter the name of the phase-shift channel for output mode
     1',I3,':',/,'  (maximal eight characters)')
   27 FORMAT ('Enter the name of the attenuation channel for output mode
     1',I3,':',/,'  (maximal eight characters)')
   28 FORMAT ('Output mode',I3,' combines how many single-transmitter mo
     1des?')
   29 FORMAT ('For output mode',I3,' enter the index of single-transmitt
     1er mode',I3,/,23X'and the borehole-compensation weight:')
   31 FORMAT (A80)
   32 FORMAT (A10)
   33 FORMAT (A2)
   34 FORMAT (A1)
   35 FORMAT (I3,F7.2,3F7.3,I3)
   36 FORMAT (I3,F7.1,3F7.2)
   37 FORMAT (2I5,3X,A2)
   38 FORMAT (10(I3,F7.2))
   39 FORMAT (2I5,3X,2A10)
   41 FORMAT ('Sonde description from 2016 SPWLA catalogue by No-Hidden-
     1Pay 2022.')
   43 FORMAT (I2,' single-transmitter, raw-measurement modes:',/,'Indice
     1s for mode, T, R1, R2, Freq',/,' Mode    T   R1   R2 Freq')
   51 FORMAT ('Operation Completed Successfully')
C
   44 FORMAT ('+----------------------+')
   45 FORMAT ('| nohiddenpay (c) 2022 |')
   46 FORMAT ('| Built using AI : Actual Intelligence (TM) |')
   47 FORMAT (' ')
   48 FORMAT ('+----------------------+--------------------+')
   53 FORMAT ('|                                           |')
   49 FORMAT ('| Tool Description Maker v1.3               |')
   54 FORMAT ('+-------------------------------------------+')
C
      WRITE (6,44)
      WRITE (6,45)
      WRITE (6,48)
      WRITE (6,46)
      WRITE (6,54)
      WRITE (6,53)
      WRITE (6,49)
      WRITE (6,53)
      WRITE (6,54)
C   Initialize the text variables: 
      DO 10 I=1,80
        FILOUT(I:I)=' '
        HEADER1(I:I)=' '
        HEADER2(I:I)=' '
   10  CONTINUE
C
C   Read the file-header information: 
   20 WRITE (6,1)
      READ (5,31) HEADER1
      DO 30 I=80,1,-1
        IF (HEADER1(I:I).NE.' ') GOTO 40
   30  CONTINUE
      GOTO 20
   40 WRITE (6,2)
      READ (5,31) HEADER2
      DO 50 J=80,1,-1
        IF (HEADER2(J:J).NE.' ') GOTO 60
   50  CONTINUE
      GOTO 40
C   Prepare and open the sonde-description output file and write the header 
C   lines in there:
   60 FILOUT=HEADER2
      FILOUT((J+1):(J+4))='.sde'
      HEADER1((I+2):(I+J+1))=HEADER2(1:J)
      OPEN (UNIT=7,STATUS='UNKNOWN',FILE=FILOUT)
      WRITE (7,31) HEADER1
      WRITE (7,41)
C   Enter length scale and other global tool information: 
      WRITE (6,3)
      READ (5,33) LSCALE
      WRITE (7,33) LSCALE
      WRITE (6,4)
      READ (5,34) YN
      IF ((YN.EQ.'Y').OR.(YN.EQ.'y')) THEN
        WRITE (6,5)
        READ (5,*) R1T(1),R2T(1),R3T(1)
        IF (R1T(1).EQ.0.0D0) R1T(1)=R3T(1)-5.0D-1
        IF (R2T(1).EQ.0.0D0) R2T(1)=R3T(1)-2.0D-1
        WRITE (6,6)
        READ (5,*) NTT(1)
        IF (NTT(1).EQ.0) NTT(1)=10
       ENDIF
C   Read all transmitter information: 
      WRITE (6,11)
      READ (5,*) NT
      DO 70 IT=1,NT
        WRITE (6,12) IT
        READ (5,*) ZT(IT)
        IF ((YN.EQ.'Y').OR.(YN.EQ.'y')) THEN
          R1T(IT)=R1T(1)
          R2T(IT)=R2T(1)
          R3T(IT)=R3T(1)
          NTT(IT)=NTT(1)
         ELSE
          WRITE (6,5)
          READ (5,*) R1T(IT),R2T(IT),R3T(IT)
          IF (R1T(IT).EQ.0.0D0) R1T(IT)=R3T(IT)-5.0D-1
          IF (R2T(IT).EQ.0.0D0) R2T(IT)=R3T(IT)-2.0D-1
          WRITE (6,6)
          READ (5,*) NTT(IT)
          IF (NTT(IT).EQ.0) NTT(IT)=10
         ENDIF
   70  CONTINUE
C   Read all receiver information: 
      WRITE (6,13)
      READ (5,*) NR
      DO 80 JR=1,NR
        WRITE (6,14) JR
        READ (5,*) ZR(JR)
        IF ((YN.EQ.'Y').OR.(YN.EQ.'y')) THEN
          R1R(JR)=R1T(1)
          R2R(JR)=R2T(1)
          R3R(JR)=R3T(1)
          NTR(JR)=NTT(1)
         ELSE
          WRITE (6,5)
          READ (5,*) R1R(JR),R2R(JR),R3R(JR)
          IF (R1R(JR).EQ.0.0D0) R1R(JR)=R3R(JR)-5.0D-1
          IF (R2R(JR).EQ.0.0D0) R2R(JR)=R3R(JR)-2.0D-1
          READ (5,*) NTR(JR)
          IF (NTR(JR).EQ.0) NTR(JR)=10
         ENDIF
   80  CONTINUE
C   Read all operating frequencies: 
      WRITE (6,15)
      READ (5,*) NF
      DO 90 KF=1,NF
        WRITE (6,16) KF
        READ (5,*) FREQ(KF),(EPS(KF,I),I=1,3)
   90  CONTINUE
C   Read the single-transmitter - single-frequency raw-measurement modes: 
      IF (NR.EQ.2) THEN
        NM=NT*NF
        WRITE (6,43) NM
        DO 110 KF=1,NF
          DO 100 IT=1,NT
            MM((IT+NT*(KF-1)),1)=IT
            IF (ZT(IT).GT.0.0D0) THEN
              MM((IT+NT*(KF-1)),2)=1
              MM((IT+NT*(KF-1)),3)=2
             ELSE
              MM((IT+NT*(KF-1)),2)=2
              MM((IT+NT*(KF-1)),3)=1
             ENDIF
            MM((IT+NT*(KF-1)),4)=KF
            WRITE (6,22) (IT+NT*(KF-1)),(MM((IT+NT*(KF-1)),I),I=1,4)
  100      CONTINUE
  110    CONTINUE
       ELSE
        WRITE (6,23)
        READ (5,*) NM
        DO 120 LM=1,NM
          WRITE (6,24) LM
          READ (5,*) (MM(LM,I),I=1,4)
  120    CONTINUE
       ENDIF
C   Read the borehole-compensated output modes: 
      WRITE (6,25)
      READ (5,*) NO
      DO 150 MO=1,NO
C   Read the names of the output modes from the SPWLA catalogue: 
        WRITE (6,26) MO
        READ (5,32) NAME(2*MO-1)
        WRITE (6,27) MO
        READ (5,32) NAME(2*MO)
C   Adjust the names of the output modes: 
        NAME(2*MO-1)(10:10)=' '
        NAME(2*MO)(10:10)=' '
        DO 130 I=9,1,-1
          NAME(2*MO-1)((I+1):(I+1))=NAME(2*MO-1)(I:I)
          NAME(2*MO)((I+1):(I+1))=NAME(2*MO)(I:I)
  130    CONTINUE
        NAME(2*MO-1)(1:1)=' '
        NAME(2*MO)(1:1)=' '
        WRITE (6,28) MO
        READ (5,*) MBHC(1,MO)
        DO 140 LM=1,MBHC(1,MO)
          WRITE (6,29) MO,LM
          READ (5,*) MBHC((LM+1),MO),BHC(LM,MO)
  140    CONTINUE
  150  CONTINUE
C
C   Write the collected tool-description data to the output file: 
      WRITE (7,22) NT,NR,NF,NM,NO
      DO 210 IT=1,NT
        WRITE (7,35) IT,ZT(IT),R1T(IT),R2T(IT),R3T(IT),NTT(IT)
  210  CONTINUE
      DO 220 JR=1,NR
        WRITE (7,35) JR,ZR(JR),R1R(JR),R2R(JR),R3R(JR),NTR(JR)
  220  CONTINUE
      DO 230 KF=1,NF
        WRITE (7,36) KF,FREQ(KF),(EPS(KF,I),I=1,3)
  230  CONTINUE
      DO 240 LM=1,NM
        WRITE (7,22) LM,(MM(LM,I),I=1,4)
  240  CONTINUE
      DO 250 MO=1,NO
C   Deactivated command lines giving phase shift and attenuation as separate, 
C   real-valued output modes. 
CX        WRITE (7,37) (2*MO-1),MBHC(1,MO),'PS'
CX        WRITE (7,38) (MBHC((LM+1),MO),BHC(LM,MO),LM=1,MBHC(1,MO))
CX        WRITE (7,37) (2*MO),MBHC(1,MO),'AT'
CX        WRITE (7,38) (MBHC((LM+1),MO),BHC(LM,MO),LM=1,MBHC(1,MO))
C   These command lines write phase shift and attenuation as combined, complex-
C   valued output modes. 
        WRITE (7,39) MO,MBHC(1,MO),NAME(2*MO-1),NAME(2*MO)
        WRITE (7,38) (MBHC((LM+1),MO),BHC(LM,MO),LM=1,MBHC(1,MO))
  250  CONTINUE
C
      CLOSE (UNIT=7)
      WRITE (6,51)
      END

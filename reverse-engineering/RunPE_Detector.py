#!/usr/bin/python
# RunPE Detector
# v 0.1
# By Kevin Falcoz (aka 0pc0deFR)
# Le code original https://github.com/Th4nat0s/Chall_Tools/blob/master/crytporacle.py
# GNU GPL V2

import struct, sys

CONSTANTES = [
[ 'SuspendThread', [ 0x53757370656e64546872656164]],
[ 'SetThreadContext', [ 0x536574546872656164436f6e74657874]],
[ 'GetThreadContext', [ 0x476574546872656164436f6e74657874]],
[ 'WriteProcessMemory', [ 0x577269746550726f636573734d656d6f7279]],
[ 'ReadProcessMemory', [ 0x5265616450726f636573734d656d6f7279]],
[ 'VirtualAllocEx', [ 0x5669727475616c416c6c6f634578]],
[ 'VirtualAlloc', [ 0x5669727475616c416c6c6f63]],
[ 'CreateProcessA', [ 0x43726561746550726f6365737341]],
[ 'VirtualProtectEx', [ 0x5669727475616c50726f746563744578]],
[ 'VirtualQueryEx', [ 0x5669727475616c51756572794578]],
[ 'ZwUnmapViewOfSection', [ 0x5a77556e6d6170566965774f6653656374696f6e]],
[ 'NtUnmapViewOfSection', [ 0x4e74556e6d6170566965774f6653656374696f6e]],
[ 'NtReadVirtualMemory', [ 0x4e74526561645669727475616c4d656d6f7279]],
[ 'NtWriteVirtualMemory', [ 0x4e7457726974655669727475616c4d656d6f7279]],
[ 'NtGetContextThread', [ 0x4e74476574436f6e74657874546872656164]],
[ 'NtSetContextThread', [ 0x4e74536574436f6e74657874546872656164]],
[ 'NtResumeThread', [ 0x4e74526573756d65546872656164]],
[ 'ResumeThread', [ 0x526573756d65546872656164]]
]

if __name__ == '__main__':

  if len(sys.argv) < 2:
    print 'RunPE Detector by Kevin Falcoz (aka 0pc0deFR)'
    print 'Examples:'
    print sys.argv[0] + ' myexefile'
    sys.exit()

  fromfile = sys.argv[1]
  
  with open(fromfile, 'rb') as f:
   filearray = bytearray(f.read())
  COUNTER = 0
  TOTAL_API = 18
  for CONST in CONSTANTES:
    print 'Checking ' + CONST[0],
    VALCOUNT = 0
    VALFOUND = 0
    for VALUES in CONST[1]:
      VALCOUNT = VALCOUNT + 1
      for I in range (0, len(filearray) - 8):
        DWORD = struct.unpack('L',str(filearray[I:I+4]))[0]
        if DWORD == VALUES:
          VALFOUND = VALFOUND + 1
          break
    if VALFOUND <> VALCOUNT:
      VALCOUNT = 0
      VALFOUND = 0
      for VALUES in CONST[1]:
        VALCOUNT = VALCOUNT + 1
        val = 0
        for i in range(0,4):
          d = VALUES & 0xFF
          val |= d << (8 * (4 - i - 1) )
          VALUES >>= 8
        VALUES = val
        for I in range (0, len(filearray) - 8):
          DWORD = struct.unpack('L',str(filearray[I:I+4]))[0]
          if DWORD == VALUES:
            VALFOUND = VALFOUND + 1
            break
    if VALFOUND:
		print 'Detected!'
		COUNTER = COUNTER + 1
    else:
        print 'Not detected!'
  PERCENT = str( ( COUNTER * 100) / TOTAL_API )
  print 'A RunPE was detected: '+PERCENT+'%'

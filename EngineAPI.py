# _*_ coding:utf-8 _*_
import glob
import mmap
import os
import hashlib

class EngineInstance:
    def _TweezerCompareEngine(self, strMalSig, strBenignFileBuf):
        nMalSigSize = len(strMalSig)

        for strSig in strMalSig:
            nCount = 0
            if nMalSigSize > nCount:
                if strSig[nCount] in str(strBenignFileBuf):
                    return True
                else:
                    return False

    def _SizeCompareEngine(self, nMalSize, nTargetSize):
        if nTargetSize == nMalSize:
            return True
        else:
            return False

    def _HashCompareEngine(self, vecMalDB, strBenignFileHash):
        for strMalDBData in vecMalDB:
            if vecMalDB[0] == strBenignFileHash:
                return True, vecMalDB[1]
        return False, ''


    def _ScanEngine(self, vecMalDB, nMalSize, vecMalSig, vecBenignFileDirList):
        bSizeRes, bTweezRes, bHashRes = 'False', 'False', 'False'
        vecScanResList = []
        vecSafeResList = []

        try:
            for strBenignFilePath in vecBenignFileDirList:
                nBenignFileSize = os.path.getsize(strBenignFilePath)

                hFile = open(strBenignFilePath, 'rb')
                strFileBuf = hFile.read()
                hFile.close()

                strTempHash = hashlib.md5()
                strTempHash.update(strFileBuf)
                strBenignfHash = strTempHash.hexdigest()

                """ Execute each ScanEngine """
                bSizeRes = self._SizeCompareEngine(nMalSize, nBenignFileSize)
                bTweezRes = self._TweezerCompareEngine(vecMalSig, strBenignfHash)
                bHashRes, strMalName = self._HashCompareEngine(vecMalDB, strBenignfHash)

                if bSizeRes == True:
                    if (bTweezRes == True) or (bHashRes == True):
                        vecTempScanList = []
                        vecTempScanList.append(strBenignFilePath)
                        vecTempScanList.append(strBenignfHash)
                        vecScanResList.append(vecTempScanList)
                else:
                    vecSafeResList.append(strBenignFilePath)
            return True, vecScanResList, vecSafeResList
        except IOError:
            return False, None, None

    def CureEngine(self, vecToCurePathList):
        try:
            while("[ERROR] Invalid command entered."):
                strConfirm = str(input("\n[?] Do you want to cure(remove) suspect file? [Y/n] : ")).lower().strip()

                if strConfirm[0] == "Y" or strConfirm[0] == "y" or strConfirm[0] == "":
                    for strCureFiledir in vecToCurePathList:
                        os.remove(strCureFiledir[0])
                    return True
                elif strConfirm[0] == "N" or strConfirm[0] == "n":
                    print("[WARN] ", "Suspect files are not cured.")
                    print("\t undispatched file count : ", len(vecToCurePathList))
                    return False
        except FileExistsError:
            return False
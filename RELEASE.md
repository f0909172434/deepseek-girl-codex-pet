# 版本安裝包與還原

分發版本是 **0.1.0**；`spriteVersionNumber: 2` 是動畫格式，兩者不相等。

到 [v0.1.0 release](https://github.com/f0909172434/deepseek-girl-codex-pet/releases/tag/v0.1.0)
下載 ZIP 與同頁的 `SHA256SUMS`。解壓前執行：

```powershell
Get-FileHash .\deepseek-girl-codex-pet-0.1.0.zip -Algorithm SHA256
```

確認結果與 release 的 `SHA256SUMS` 相同，再解壓並執行
`powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1`。
安裝器會先驗證圖集，再備份並複製檔案。備份預設放在 `.codex\pet-backups`，
位於寵物掃描目錄之外。測試時可用 `-DestinationDir` 與 `-BackupRoot` 指定暫存目錄。

## 移除與還原

先關閉 Codex Desktop。將 `.codex\pets\deepseek-girl-codex-pet` 移到
`.codex\pet-backups\deepseek-girl-codex-pet.disabled`，保留檔案並移出 `pets` 掃描目錄。
若要還原先前版本，將安裝器輸出的 `.backup-日期時間` 目錄移回原安裝路徑，
再重新啟動 Codex。先確認目的名稱不存在，避免覆寫另一份安裝。

## 重現與驗證範圍

Python 3.12，不需要第三方套件：

```sh
python scripts/verify.py
python -m unittest discover -s scripts -p "test_*.py" -v
python scripts/package.py
```

包裝使用固定時間、排序白名單與固定檔案權限。CI 在 Ubuntu 與 Windows
各自連續打包兩次並比較 bytes；Windows 另外把安裝、再次安裝與備份測試放在
暫存目錄，不改動真實的 Codex 安裝。

這些檢查涵蓋圖集、manifest、檔案完整性及安裝腳本。圖集的完整視覺 QA
另見 `qa/atlas-validation.json`。自訂寵物路徑仍是觀察到的本機介面，
沒有公開的官方相容性契約；封裝測試不等於當前所有 Codex 版本都能載入。

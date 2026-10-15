# SEO / GEO Evidence Skill

An open, portable skill for source-backed SEO, generative search visibility and editorial decisions. 以可追溯來源規劃內容、搜尋呈現與量測；不承諾排名或引用。

## 安裝／使用

將本倉庫的 `skills/seo-geo-evidence` 完整資料夾放進你的工具支援的 skills 目錄。請依客戶端當前官方文件確認目錄與載入方式，不需要執行遠端安裝腳本。

- Codex：使用支援的 skill 安裝流程，或放入專案的 `.agents/skills/`。
- Claude Code：可放入專案 `.claude/skills/`，仍需依該版本確認是否載入。
- 網頁聊天：若不能安裝 skill，將 SKILL.md 與本次相關 references 作為附件；附檔是內容快照，不等於自動啟用工具或自動更新。

範例：`使用 seo-geo-evidence 檢視這篇文章，分開說明搜尋資格、AI引用、訪問量；列來源與未驗證項目。`

## 結構與來源

技能本體在 `skills/seo-geo-evidence/`；只讀本次需要的 reference。`references/sources.json` 保存原來源、種類及最後查核日。初版移植自已整理的公開精選知識，來源快照為2026-10-13；建立skill日期為2026-10-15，沒有將舊來源日期改成今天。

`references/provenance.json` 僅記錄首次移植雜湊，並非新版即時完整性manifest。此倉庫是skill的版本來源；既有知識網站是另一個已發布快照，不會因Git更新自動同步。

## 每月維護

每月研究Google官方文件、GitHub相關skills、YouTube、X與Threads的公開資料。先整理證據與差異，再修改候選版本，經獨立檢查後才提出發布。方法、界線與狀態格式見 [maintenance/MONTHLY.md](maintenance/MONTHLY.md)。未完成的搜尋不能被寫成「沒有新消息」。

`python3 scripts/validate.py` 執行本機發布檢查，不連網、不執行第三方skill。

## 授權

本倉庫原創指令、程式與整理文字採MIT。外部官方文件、論文、影片、貼文及其他倉庫保留各自權利；連結不代表重授權。第三方內容先獨立理解與核對；若確實重用程式或文字，另遵守其授權與歸屬要求。

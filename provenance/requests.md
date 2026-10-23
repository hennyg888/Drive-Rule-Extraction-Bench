# Requests behind the reference ruleset

These are michael's messages in the project thread that shaped the passing rules, copied verbatim, with times in UTC. The thread is the project's "Wise Lab" passing-rules thread on claude.ai; the replies Claude wrote in between are not repeated here. Messages after 11 October 2026 04:40 asked about the review page, the VLA and the Qwen handoff and did not change any statement.

Two more inputs came from michael on 10 October:

- At 21:47 he posted a table of rule templates in the project chat, saved as [inputs/template-table-2026-10-10.png](inputs/template-table-2026-10-10.png). Its patterns (MUST / MUST NOT … WHEN … UNLESS, MAY … ONLY IF, TO goal: steps; DONE WHEN; IF event THEN, WATCH FOR, IS … THAT, SPECIALIZES, BECAUSE) are the starting point of the v0 template plan and of rule language v1.
- His Passing Topic Comparison page (https://claude.ai/artifact/A8gZroLVV8miAsmAym44C6) held the 96 passages, their grouping into sections and their notes. Its data is in `analysis/passing-rules/inputs/`.

## 2026-10-10 21:42

This is a lab project that the objective is to extract ("transform") driving rules from MTO Driver's handbook into a set of "formal rules". 

- Formal rules mean there are some predefined syntax and template for representing the rule instructions. Such as SQL for database language and LTL for some symbolic language.
- However, in this project, I just want to get rid of the LTL-style formalized rules, since I think it isn't a good representation for LLM/VLM to reason over compared to "natural-language"-like styles.

We can start from the overtaking (passing) section inside the handbook. https://www.ontario.ca/document/official-mto-drivers-handbook/changing-positions

My current idea is to first understand and analysis the content structure of the handbook. I hypothsize that it was written in some principles. 
For example,
- https://www.ontario.ca/document/official-mto-drivers-handbook/changing-positions 像這一頁就有很明確的 instruction (rules) 。
- 我想先試圖理解他這個 driving handbook 的 "content structure"，他們應該有個 "predefined" 的編寫架構與組織
- 以這個 passing 來說，他們會先講說明一些 "formal definition"，再來介紹一下 "passing" 的 general concept 是什麼、正常過程應該怎麼做 (steps for passing a vehicle)。有什麼限制與注意事項："Passing within 30 metres of a pedestrian crossover is not permitted. Passing left of a centreline is not permitted 30 metres from a bridge, viaduct or tunnel. Don't attempt to pass when approaching the crest of a hill or on a curve where your vision of oncoming traffic is obstructed and there is not enough clear distance ahead to pass in safety.
  When passing parked vehicles, watch carefully for people suddenly opening doors or for doors opened to load and unload.
  Motorcycles, bicycles, limited-speed motorcycles and mopeds often need to pull to the left or right side of their lane to avoid dangerous road conditions or to be seen by other drivers. Do not take this as an invitation to pass in the same lane. If you do want to pass these vehicles, do so by changing lanes.
  When faster traffic wants to pass you, move to the right and let it pass in safety. When being passed on an undivided road where the passing driver has pulled into the opposite lane, pay attention to oncoming traffic and move closer to the right side of the lane. Be prepared to slow down to let the passing driver get in front of you more quickly to prevent a collision.
  On many high-speed roads with three or more lanes in each direction, trucks are not allowed to drive in the far left-hand lane. This means that the lane next to it is the truck passing lane. If you are in this lane and a truck wants to pass, move into the right-hand lane as soon as you can."
- 有了以上的 “general concept” 之後，才接著列舉說 passing 的其他 special condition? 會有哪些情況，以及各個情況各自的 condition 是什麼、注意事項、操作流程是什麼、能 or 不能怎麼做
先來跟我一起整理一下這個 content structure 出來？我們一步一步把它 structure 化

---
已經有整理出目前的版本了：https://claude.ai/artifact/A8gZroLVV8miAsmAym44C6，你可以看一下

我跟我組員也討論了一下，他覺得應該可以把我們現在做的這個 preprocessing 的事情當作 human verification 的內容。這些 preprocessing 應該可以直接包在 VLM extraction，變成是把整個 handbook 直接丟給 VLM，讓他自己做這些 cross-reference linking、information gathering 之類的事情，然後直接得到 formalized rules

## 2026-10-10 21:57

* 那我們現在要做的事情就是先規劃一些 formal rule templates (similar to SQL style, with specific/predefined patterns and wordings.)。我希望是 natural-language-like style，不是 LTL 那種 symbolic style，因為 LLM is better at reason over natural-language-like context
* 但我們要決定的 rule templates 可能需要掃完整本 handbook 才知道我們要設計哪些 patterns/wordings? 我希望用一個最小的 set 去做到，就像 SQL 也是用一些小集合的 wording 去設計他們的 syntax。
* content in the handbook 可能會有一些模糊的地方，可以先 highlight 起來我們之後再來想怎麼處理

你可以先幫我規劃或是完善一下這個計畫，我們先討論看看有什麼好的做法與 rule template

## 2026-10-10 21:58

以及過去的文章有沒有可以參考的設計，也需要你去 search 一下 recent & prior relevant works

## 2026-10-10 22:09

This answers four questions at the end of Claude's plan (`analysis/rule-template-plan.md` §7): 1. make cautions their own type, or fold them into `SHOULD WATCH FOR`; 2. default bare imperatives to SHOULD, raising to MUST only on legal wording; 3. write exceptions with UNLESS in the same sentence and EXCEPTION TO across passages; 4. scope (chapters 2 and 3 first?).

1. 可以先併進去 should watch for
2. ok
3. ok
4. 一樣先從 overtaking (passing) 開始做就好，但你的 keyword 仍然需要先去做 full book scanning 去規劃 wording & template you are going to use。


你整理完的 rule 我希望可以用我們剛剛產生的: https://claude.ai/artifact/A8gZroLVV8miAsmAym44C6 頁面一樣，可以左右對照著看

## 2026-10-10 23:24

* 右半邊的 rule 視覺化沒有很好閱讀。那些 sentence 裡面的 key words 應該也要用這種有 border 的 style 表示出來，比較好閱讀
* 以及 rule 之間的排版也可以調整一下增加人類的易讀性，可以有淺底色的 block 表示 single rule 增加段落感
* 不同 section (e.g., 3. 特定情境下的指引, 3.1
地點、標線與標誌...) 也可以用更好的 UI 增加易讀性，想像你在建立一個 modern. elegant website

## 2026-10-11 01:46

要不要在前面先有一個 overall 的 template, wording 介紹？畢竟我們的重點也在提出一個好的 natural-language-like formal rule

## 2026-10-11 02:27

可以幫我做成分頁的形式嗎

## 2026-10-11 02:37

並且幫我保留重點就好、內容維持精簡，不需要太多篇幅，應該用最小的篇幅就可以表達完整全面的意思

## 2026-10-11 03:10

你可做成像左邊有個書籤或是 table of content 那樣

## 2026-10-11 03:14

Law 的可以幫我換成紅色，advice 換成黃色，definition 換成綠色，vague 換成藍色？

## 2026-10-11 03:53

* 這些是不是放在第一頁就好？
* 以及我說的比較像是 navigation panel 在左側
* 語言的話可以預設是英文 (English 在左邊、中文在右邊)

## 2026-10-11 04:00

以及你現在的 rule 好像沒有順便把原始圖片一起放在一起，應該要放在一起？可以放在對應的 rule 底下?

## 2026-10-11 04:37

以及讓左右兩邊的 content 點一下可以跳到另外一方的 content，現在只有 hover 過去會顯示對應的 original/rule 而已

## 2026-10-10 23:00, decision card (Claude asked, michael chose)

Question: 加入全書掃描找到、不在你 96 段裡的 8 句超車規則?

Context: 這 8 句在其他頁。Stopping 頁 5 句校車規則:校車上方紅燈閃時必須停車、從後方來要停在 20 m 外、等校車開走或燈停才能走、有中央分隔島時只有後方來車要停、違規記 6 點。Changing directions 頁 2 句:左轉時不要開到前面轉彎的機車或腳踏車旁邊一起轉。Signs 頁 1 句:多車道上的慢車必須靠右。目前規則集裡校車只有一句 FACT(可以檢舉違規超越校車的車),真正的法規不在裡面。

- 加入: 我把 8 句寫成規則放進對應段落,左欄最後加一區「其他頁」,用同一個連結更新頁面和 JSON。
- 先不加: 規則集維持你 96 段的範圍,這 8 句留在頁面的「全書掃描找到的」區。

michael chose "加入" at 23:04. The 8 sentences became 7 statements: 3.4.3b, 3.4.3c, 3.4.12b to 3.4.12e and 3.6.1d (inputs c1 to c9, with the sign image as c9).

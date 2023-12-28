; Read name from ThisWeek.txt on the desktop
;desktopPath := A_Desktop . "\\이번주 소스담당자.txt"
;if not FileExist(desktopPath)
;{
;    MsgBox, % "File not found: " . desktopPath
;   return
;}
;FileRead, fileContent, %desktopPath%
;RegexMatch(fileContent, "name = (.*?)(`r`n|$)", name)

; Bone 주사시간 & 이름
^!a::
WinWaitActive,BRMH _PaperList 작성 -- 웹 페이지 대화 상자
WinActive(BRMH _PaperList 작성 -- 웹 페이지 대화 상자)
WinMove 0,0
    Click 218, 371
    Click 218, 395, 4
    SendInput 20
    Click 218, 420,4
    FormatTime, CurrentTime,, HH:mm
    SendInput %CurrentTime%
    Click 218, 490, 4
    Sendinput 김계환
return

; 환자 Call 방송
^!c::
    ; 현재 마우스 위치에서 왼쪽 클릭을 수행합니다.
    ; MouseClick, left  
    
    ; 텍스트를 복사하기 전에 잠시 기다립니다. 필요에 따라 시간을 조정하세요.
    Send, ^c
    
    ; 지정된 제목의 창을 활성화합니다.
    WinActivate, 주사실 환자 호출    
    Sleep, 100

    ; 마우스를 창 내의 좌표 (30, 80)로 이동합니다.
    MouseMove, 55, 120, 0

    ; 붙여넣기 전에 잠시 기다립니다. 필요에 따라 시간을 조정하세요.
    Sleep, 100
    MouseClick, left  

    ; 오른쪽 클릭으로 컨텍스트 메뉴를 엽니다.
    Send, ^v
    Sleep, 100
    Send, {Enter}
Return

;현재시간 입력
^!s::
    Click, 2
    FormatTime, CurrentTime,, HH:mm
    SendInput %CurrentTime%
Return

;이름 입력
^!d::
    Click, 2
    SendInput %name%
Return

;HIS 로그인
^!h::
; Read id and pw from ThisWeek.txt on the desktop
desktopPath := A_Desktop . "\\이번주 소스담당자.txt"
if not FileExist(desktopPath)
{
    MsgBox, % "File not found: " . desktopPath
    return
}

FileRead, fileContent, %desktopPath%
RegexMatch(fileContent, "id = (.*?)(`r`n|$)", id)
RegexMatch(fileContent, "pw = (.*?)(`r`n|$)", pw)

WinWaitActive,#BRMH 보라매병원 통합의료정보시스템# - Internet Explorer
WinActive(#BRMH 보라매병원 통합의료정보시스템# - Internet Explorer)

    Click 1230, 724
    Sleep, 100
    SendInput %id1%
    Sleep, 100
    Click 1230, 760

    Sendraw %pw1%
    Sleep, 200
    Click 1251, 813

;핵의학체내
    WinWaitActive,BRMH 보라매병원 통합의료정보시스템 100.11.1.85 - Internet Explorer
    Winactive(BRMH 보라매병원 통합의료정보시스템 100.11.1.85 - Internet Explorer)
    Sleep, 200
    Click 972,280

WinWaitActive, BRMH - Internet Explorer
Winmove, BRMH - Internet Explorer,, 0,0
Winactive(BRMH - Internet Explorer)
;검사실시관리
    Sleep, 2000
    Click 125, 155, 2
;검사진행조회
    Sleep, 500
    Click 154, 500, 2 

;NM 조회
WinWaitActive, BRMH _검사진행조회_Xray - Internet Explorer
Winactive(BRMH _검사진행조회_Xray - Internet Explorer)
    Sleep,500
    Click 391, 84
    SendInput NM
    Sleep, 200
    Click 843, 81
    Sleep, 200
    Click 1121, 80
Return       


F2::Pause
F4::ExitApp
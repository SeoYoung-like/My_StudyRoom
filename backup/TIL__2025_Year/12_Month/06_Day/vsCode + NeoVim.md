# vsCode + NeoVim

(Vim 설치 실패시 - 에러 발생할 경우) Reset 전체 삭제 

환경 : Window 10



**[ Vim => NeoVim 사용 이유 ]**

VS에서 느려지고, 멈추는 버그가 있음



**[ 설치 방법 ]**

1. 홈페이지에서 OS에 맞는 NeoVim다운로드

2. VS Extension에서 설치

3. VS 환경설정 ( `Ctrl + ,` ) 

   1. neovim 검색
   2. Window 환경 - `Vscode-neovim › Neovim Executable Paths: Win32` : 실행 파일 기입
      * 실행파일 주소 찾는법 - 터미널 : `where nvim` 입력

4. 재시작

5. vim 과 window 클립보드 연동을 위한 세팅 필요 - 필수 세팅

   * 현재 : vim extension 다운로드 => vim `Use System Clipboard` 활성화

   * 다른 방법 : 

     *  **Neovim에서 시스템 클립보드(복사/붙여넣기)를 사용할 수 있게 하는 설정**

     * init.vim(또는 .vimrc)에 명령어를 추가 해준다.

     * ```
       set clipboard+=unnamedplus
       ```






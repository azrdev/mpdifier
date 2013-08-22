#include <windows.h>

int pressKey(WORD keyCode)
{
    UINT rv = 2;

    // This structure will be used to create the keyboard input event.
    INPUT ip;
 
    // Set up a generic keyboard event.
    ip.type = INPUT_KEYBOARD;
    ip.ki.wScan = 0; // hardware scan code for key
    ip.ki.time = 0;
    ip.ki.dwExtraInfo = 0;
 
    // Press the key
    ip.ki.wVk = keyCode;
    ip.ki.dwFlags = 0; // 0 for key press
    rv -= SendInput(1, &ip, sizeof(INPUT));
 
    // Release the key
    ip.ki.dwFlags = KEYEVENTF_KEYUP; // KEYEVENTF_KEYUP for key release
    return rv - SendInput(1, &ip, sizeof(INPUT));
}
 
int main(int argc, char* argv[])
{
    if(argc < 2) {
        return 1;
    }

    switch(argv[1][0]) {
        case '+':
            return pressKey(VK_VOLUME_UP);
        case '-':
            return pressKey(VK_VOLUME_DOWN);
        case 'm':
            return pressKey(VK_VOLUME_MUTE);

        case 't':
            return pressKey(VK_MEDIA_PLAY_PAUSE);
        case 'n':
            return pressKey(VK_MEDIA_NEXT_TRACK);
        case 'p':
            return pressKey(VK_MEDIA_PREV_TRACK);
        case 's':
            return pressKey(VK_MEDIA_STOP);
    }
    return 1;
}

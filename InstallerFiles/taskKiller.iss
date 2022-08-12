[Code]
procedure TaskKill();
var
  ResultCode: Integer;
begin
    Exec('taskkill.exe', '/f /im ' + '"' + 'EasyMinecraftServer.exe' + '"', '', SW_HIDE,
     ewWaitUntilTerminated, ResultCode);
    Exec('taskkill.exe', '/f /im ' + '"' + 'mcserver.exe' + '"', '', SW_HIDE,
     ewWaitUntilTerminated, ResultCode);
    Exec('taskkill.exe', '/f /im ' + '"' + 'MinecraftServerElevator.exe' + '"', '', SW_HIDE,
     ewWaitUntilTerminated, ResultCode);
    Exec('taskkill.exe', '/f /im ' + '"' + 'MinecraftServerUnelevator.exe' + '"', '', SW_HIDE,
     ewWaitUntilTerminated, ResultCode);
    Exec('taskkill.exe', '/f /im ' + '"' + 'MinecraftServerGUI.exe' + '"', '', SW_HIDE,
     ewWaitUntilTerminated, ResultCode);
    Exec('taskkill.exe', '/f /im ' + '"' + 'MinecraftServer-nogui.exe' + '"', '', SW_HIDE,
     ewWaitUntilTerminated, ResultCode);
    Exec('taskkill.exe', '/f /im ' + '"' + 'SecretManager.exe' + '"', '', SW_HIDE,
     ewWaitUntilTerminated, ResultCode);
    Exec('taskkill.exe', '/f /im ' + '"' + 'ServerAutoBackup.exe' + '"', '', SW_HIDE,
     ewWaitUntilTerminated, ResultCode);
    Exec('taskkill.exe', '/f /im ' + '"' + 'ngrok.exe' + '"', '', SW_HIDE,
     ewWaitUntilTerminated, ResultCode);
end;
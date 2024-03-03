{ pkgs }: {
    deps = [
      pkgs.geckodriver
      pkgs.cowsay
      pkgs.chromium
      pkgs.chromedriver
    ];
}
{
  description = "Multi-environment Bazel and CodeChecker tests";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux"; # Or "aarch64-darwin", etc.
      pkgs = import nixpkgs { inherit system; };

      codechecker = pkgs.codechecker; 
      bazelVersions = {
        # bazel_6 = pkgs.bazel_6;
        bazel_7 = pkgs.bazel_7;
        bazel_8 = pkgs.bazel_8;
      };

      # Function to create a test derivation for a specific Bazel version
      mkBazelTest = name: bazelPkg: pkgs.stdenv.mkDerivation {
        name = "test-env-${name}";
        src = ./.; # The source code of your project

      __noChroot = true;

        # Tools available during the test
        nativeBuildInputs = [ 
          bazelPkg
          codechecker
          pkgs.clang
          pkgs.python3
          pkgs.python3Packages.pytest
          pkgs.gcc
        ];

        doCheck = true;

        # The actual test commands
        checkPhase = ''
          echo "Running tests with ${bazelPkg.name} and ${codechecker.name}"
          # Must be set for Bazel's cache 
          mkdir -p .tmp_bazel
          export TMPDIR=$(pwd)/.tmp_bazel

          export TEST_TMPDIR=$TMPDIR
          export BAZEL_OUTPUT_BASE=$TMPDIR/bazel_out
          CodeChecker version
          bazel version
          clang --version
          clang-extdef-mapping --version
          clang-tidy --version

          pytest test/unit -vvv
        '';

        # Derivations must produce an output file to be considered "built"
        installPhase = "touch $out";
      };

    in {
      # This generates: checks.x86_64-linux.bazel_6, etc.
      checks.${system} = builtins.mapAttrs mkBazelTest bazelVersions;
    };
}

from collections import defaultdict

ICONS_TYPE_FILES_ICONIFY = {
    # Lenguajes de programación
    **dict.fromkeys(["py"], "https://api.iconify.design/vscode-icons:file-type-python.svg"),
    **dict.fromkeys(["c"], "https://api.iconify.design/vscode-icons:file-type-c.svg"),
    **dict.fromkeys(["cpp"], "https://api.iconify.design/vscode-icons:file-type-cpp.svg"),
    **dict.fromkeys(["h"], "https://api.iconify.design/vscode-icons:file-type-cheader.svg"),
    **dict.fromkeys(["hpp"], "https://api.iconify.design/vscode-icons:file-type-cppheader.svg"),
    **dict.fromkeys(["java"], "https://api.iconify.design/vscode-icons:file-type-java.svg"),
    **dict.fromkeys(["kt", "kts"], "https://api.iconify.design/vscode-icons:file-type-kotlin.svg"),
    **dict.fromkeys(["js"], "https://api.iconify.design/vscode-icons:file-type-js.svg"),
    **dict.fromkeys(["ts"], "https://api.iconify.design/vscode-icons:file-type-typescript.svg"),
    **dict.fromkeys(["go"], "https://api.iconify.design/vscode-icons:file-type-go.svg"),
    **dict.fromkeys(["rs"], "https://api.iconify.design/vscode-icons:file-type-rust.svg"),
    **dict.fromkeys(["rb"], "https://api.iconify.design/vscode-icons:file-type-ruby.svg"),
    **dict.fromkeys(["php"], "https://api.iconify.design/vscode-icons:file-type-php.svg"),
    **dict.fromkeys(["lua"], "https://api.iconify.design/vscode-icons:file-type-lua.svg"),
    **dict.fromkeys(["swift"], "https://api.iconify.design/vscode-icons:file-type-swift.svg"),
    **dict.fromkeys(["scala"], "https://api.iconify.design/vscode-icons:file-type-scala.svg"),
    **dict.fromkeys(["dart"], "https://api.iconify.design/vscode-icons:file-type-dartlang.svg"),
    **dict.fromkeys(["cs"], "https://api.iconify.design/vscode-icons:file-type-csharp.svg"),
    **dict.fromkeys(["vb"], "https://api.iconify.design/vscode-icons:file-type-vb.svg"),
    **dict.fromkeys(["m"], "https://api.iconify.design/vscode-icons:file-type-objectivec.svg"),
    **dict.fromkeys(["r"], "https://api.iconify.design/vscode-icons:file-type-r.svg"),
    **dict.fromkeys(["jl"], "https://api.iconify.design/vscode-icons:file-type-julia.svg"),

    # Scripts y configuración
    **dict.fromkeys(["sh", "bash", "zsh"], "https://api.iconify.design/vscode-icons:file-type-shell.svg"),
    **dict.fromkeys(["bat", "cmd"], "https://api.iconify.design/vscode-icons:file-type-bat.svg"),
    **dict.fromkeys(["ps1"], "https://api.iconify.design/vscode-icons:file-type-powershell.svg"),
    **dict.fromkeys(["env"], "https://api.iconify.design/vscode-icons:file-type-dotenv.svg"),
    **dict.fromkeys(["ini"], "https://api.iconify.design/vscode-icons:file-type-ini.svg"),
    **dict.fromkeys(["conf", "cfg"], "https://api.iconify.design/vscode-icons:file-type-config.svg"),
    **dict.fromkeys(["toml"], "https://api.iconify.design/vscode-icons:file-type-toml.svg"),
    **dict.fromkeys(["yaml", "yml"], "https://api.iconify.design/vscode-icons:file-type-yaml.svg"),
    **dict.fromkeys(["json", "jsonld"], "https://api.iconify.design/vscode-icons:file-type-json.svg"),
    **dict.fromkeys(["xml"], "https://api.iconify.design/vscode-icons:file-type-xml.svg"),
    **dict.fromkeys(["log"], "https://api.iconify.design/vscode-icons:file-type-log.svg"),

    # Archivos de proyecto y sistema
    **dict.fromkeys(["makefile"], "https://api.iconify.design/vscode-icons:file-type-makefile.svg"),
    **dict.fromkeys(["dockerfile"], "https://api.iconify.design/vscode-icons:file-type-docker.svg"),
    **dict.fromkeys(["gradle"], "https://api.iconify.design/vscode-icons:file-type-gradle.svg"),
    **dict.fromkeys(["gitignore", "gitattributes"], "https://api.iconify.design/vscode-icons:file-type-git.svg"),
    **dict.fromkeys(["editorconfig"], "https://api.iconify.design/vscode-icons:file-type-editorconfig.svg"),
    **dict.fromkeys(["npmrc"], "https://api.iconify.design/vscode-icons:file-type-npm.svg"),
    **dict.fromkeys(["eslintignore"], "https://api.iconify.design/vscode-icons:file-type-eslint.svg"),
    **dict.fromkeys(["babelrc"], "https://api.iconify.design/vscode-icons:file-type-babel.svg"),
    **dict.fromkeys(["prettierrc"], "https://api.iconify.design/vscode-icons:file-type-prettier.svg"),
    **dict.fromkeys(["deb"], "https://api.iconify.design/vscode-icons:file-type-debian.svg"),
    **dict.fromkeys(["exe"], "https://api.iconify.design/vscode-icons:file-type-manifest.svg"),
    **dict.fromkeys(["msi"], "https://api.iconify.design/vscode-icons:file-type-registry.svg"),
    **dict.fromkeys(["run", "bin", "out"], "https://api.iconify.design/vscode-icons:file-type-binary.svg"),

    # Web
    **dict.fromkeys(["html", "htm"], "https://api.iconify.design/vscode-icons:file-type-html.svg"),
    **dict.fromkeys(["css"], "https://api.iconify.design/vscode-icons:file-type-css.svg"),
    **dict.fromkeys(["scss", "sass"], "https://api.iconify.design/vscode-icons:file-type-sass.svg"),
    **dict.fromkeys(["less"], "https://api.iconify.design/vscode-icons:file-type-less.svg"),
    **dict.fromkeys(["vue"], "https://api.iconify.design/vscode-icons:file-type-vue.svg"),
    **dict.fromkeys(["astro"], "https://api.iconify.design/vscode-icons:file-type-astro.svg"),
    **dict.fromkeys(["svelte"], "https://api.iconify.design/vscode-icons:file-type-svelte.svg"),

    # Bases de datos
    **dict.fromkeys(["sql"], "https://api.iconify.design/vscode-icons:file-type-sql.svg"),
    **dict.fromkeys(["sqlite"], "https://api.iconify.design/vscode-icons:file-type-sqlite.svg"),
    **dict.fromkeys(["db"], "https://api.iconify.design/vscode-icons:file-type-db.svg"),
    **dict.fromkeys(["csv", "xls", "xlsx"], "https://api.iconify.design/vscode-icons:file-type-libreoffice-calc.svg"),

    # Documentación y texto
    **dict.fromkeys(["md", "markdown"], "https://api.iconify.design/vscode-icons:file-type-markdown.svg"),
    **dict.fromkeys(["txt"], "https://api.iconify.design/vscode-icons:file-type-text.svg"),
    **dict.fromkeys(["rst"], "https://api.iconify.design/vscode-icons:file-type-codekit.svg"),
    **dict.fromkeys(["adoc"], "https://api.iconify.design/vscode-icons:file-type-asciidoc.svg"),
    **dict.fromkeys(["pdf"], "https://api.iconify.design/vscode-icons:file-type-pdf2.svg"),
    **dict.fromkeys(["doc", "docx"], "https://api.iconify.design/vscode-icons:file-type-word2.svg"),
    **dict.fromkeys(["ppt", "pptx"], "https://api.iconify.design/vscode-icons:file-type-libreoffice-impress.svg"),

    # Archivos comprimidos
    **dict.fromkeys(["zip", "tar", "gz", "rar", "7z"], "https://api.iconify.design/vscode-icons:file-type-zip.svg"),
    **dict.fromkeys(["iso"], "https://api.iconify.design/carbon:iso.svg"),
    # Imágenes
    **dict.fromkeys(["png", "jpg", "jpeg", "gif", "bmp"], "https://api.iconify.design/vscode-icons:file-type-image.svg"),
    **dict.fromkeys(["svg"], "https://api.iconify.design/vscode-icons:file-type-svg.svg"),
    **dict.fromkeys(["mp4"], "https://api.iconify.design/vscode-icons:file-type-video.svg"),

    # Otros
    **dict.fromkeys(["nds"], "https://api.iconify.design/arcticons/nintendo-alt-1.svg"),
    **dict.fromkeys(["license", "MIT"], "https://api.iconify.design/vscode-icons:file-type-license.svg"),
    **dict.fromkeys(["tsconfig"], "https://api.iconify.design/vscode-icons:file-type-tsconfig.svg"),
    **dict.fromkeys(["webpack"], "https://api.iconify.design/vscode-icons:file-type-webpack.svg"),
    **dict.fromkeys(["rpm"], "https://api.iconify.design/vscode-icons:file-type-package.svg"),

    "default_file": "https://api.iconify.design/vscode-icons:file-type-light-ini.svg"
}

ICONS_TYPE_FOLDER_ICONIFY = {
    "src": ["src", "source"],
    "build": ["build"],
    "dist": ["dist"],
    "node_modules": ["node_modules"],
    "config": ["config", "configs"],
    "assets": ["assets"],
    "images": ["images", "img", "icons"],
    "fonts": ["fonts"],
    "scripts": ["scripts", "js"],
    "css": ["styles", "css"],
    "sass": ["sass"],
    "docs": ["docs", "documentation"],
    "test": ["tests", "test"],
    "examples": ["examples"],
    "bin": ["bin"],
    "lib": ["lib"],
    "public": ["public"],
    "private": ["private"],
    "env": ["env"],
    "template": ["templates", "template"],
    "server": ["server"],
    "client": ["client"],
    "database": ["database", "db"],
    "logs": ["logs"],
    "resource": ["res", "resource"],
    "data": ["data"],
    "storage": ["storage"],
    "media": ["media"],
    "Descargas": ["downloads"],
    "uploads": ["upload", "uploads"],
    "cache": ["cache"],
    "temp": ["tmp", "temp"],
    "Escritorio": ["desktop"],
    "Documentos": ["documents"],
    "Musica": ["music"],
    "Imagenes": ["pictures"],
    "Videos": ["videos"],
    "default_folder": ["folder"]
}



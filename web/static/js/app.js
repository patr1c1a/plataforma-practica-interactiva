(function () {

    let activeCodeEditor = null;

    function initializeApplication() {
        initializeTheme();
        initializeDropdown();
        initializeCodeEditor();
    }

    /* =========================
       THEME
    ========================== */

    function initializeTheme() {
        const toggleButton = document.getElementById("theme-toggle");
        if (!toggleButton) return;

        const storedTheme = localStorage.getItem("preferred-theme");
        const themeToApply = storedTheme ? storedTheme : "dark";

        applyTheme(themeToApply);

        if (!toggleButton.dataset.listenerAttached) {
            toggleButton.addEventListener("click", function () {
                const currentTheme = document.documentElement.getAttribute("data-theme");
                const newTheme = currentTheme === "dark" ? "light" : "dark";
                applyTheme(newTheme);
            });

            toggleButton.dataset.listenerAttached = "true";
        }
    }

    function applyTheme(theme) {
        const rootElement = document.documentElement;
        const toggleButton = document.getElementById("theme-toggle");

        rootElement.setAttribute("data-theme", theme);
        localStorage.setItem("preferred-theme", theme);

        if (toggleButton) {
            toggleButton.textContent = theme === "dark" ? "🌙" : "☀";
        }

        if (activeCodeEditor) {
            const newEditorTheme = theme === "dark" ? "material-darker" : "default";
            activeCodeEditor.setOption("theme", newEditorTheme);
        }
    }

    /* =========================
       DROPDOWN
    ========================== */

    function initializeDropdown() {
        const dropdown = document.querySelector(".dropdown");
        const toggle = document.querySelector(".dropdown-toggle");

        if (!dropdown || !toggle) return;

        if (!toggle.dataset.listenerAttached) {
            toggle.addEventListener("click", function (event) {
                event.stopPropagation();
                dropdown.classList.toggle("open");
            });

            document.addEventListener("click", function () {
                dropdown.classList.remove("open");
            });

            toggle.dataset.listenerAttached = "true";
        }
    }

    /* =========================
       CODE EDITOR
    ========================== */

    function initializeCodeEditor() {
        if (typeof CodeMirror === "undefined") return;

        const textarea = document.getElementById("code-editor");
        if (!textarea) return;

        // If CodeMirror was already used, do not initialize again
        if (textarea._editorInstance) {
            activeCodeEditor = textarea._editorInstance;
            return;
        }

        const currentTheme = document.documentElement.getAttribute("data-theme");
        const codeMirrorTheme = currentTheme === "dark" ? "material-darker" : "default";

        const editor = CodeMirror.fromTextArea(textarea, {
            mode: "python",
            lineNumbers: true,
            indentUnit: 4,
            tabSize: 4,
            indentWithTabs: false,
            lineWrapping: false,
            theme: codeMirrorTheme,
            extraKeys: {
                Tab: function (cm) {
                    cm.replaceSelection("    ", "end");
                }
            }
        });

        const form = textarea.closest("form");
        if (form) {
        form.addEventListener("submit", function () {
            editor.save();
        });
        }
        
        textarea._editorInstance = editor;
        activeCodeEditor = editor;

        const storageKey = textarea.dataset.storageKey;
        const savedCode = sessionStorage.getItem(storageKey);

        if (savedCode) {
            editor.setValue(savedCode);
        }

        editor.on("change", function (cm) {
            sessionStorage.setItem(storageKey, cm.getValue());
        });

        activeCodeEditor = editor;

        const totalLines = editor.lineCount();
        editor.setCursor({ line: totalLines - 1, ch: 4 });
    }

    /* =========================
       HTMX HOOKS
    ========================== */

    document.addEventListener("DOMContentLoaded", function () {
        initializeApplication();
    });

    document.body.addEventListener("htmx:afterSwap", function (event) {
        if (event.target.id === "main-content") {
            initializeCodeEditor();
        }
    });

    document.body.addEventListener("htmx:historyRestore", function () {
        initializeApplication();
    });

})();
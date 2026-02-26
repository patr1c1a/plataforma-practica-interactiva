(function () {

    let activeCodeEditor = null;

    function initializeApplication() {
        initializeTheme();
        initializeDropdown();
        initializeCodeEditor();
        updateExerciseVisualState();
        updateCategoryProgress();
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

        toggleButton.addEventListener("click", function () {
            const currentTheme = document.documentElement.getAttribute("data-theme");
            const newTheme = currentTheme === "dark" ? "light" : "dark";
            applyTheme(newTheme);
        });
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

        toggle.addEventListener("click", function (event) {
            event.stopPropagation();
            dropdown.classList.toggle("open");
        });
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
        PROGRESS
    ========================= */

    const PROGRESS_STORAGE_KEY = "platform-progress-v1";

    function loadProgress() {
        const raw = localStorage.getItem(PROGRESS_STORAGE_KEY);
        return raw ? JSON.parse(raw) : {};
    }

    function saveProgress(progressData) {
        localStorage.setItem(PROGRESS_STORAGE_KEY, JSON.stringify(progressData));
    }

    function markExerciseAttempted(category, exercise) {
        const progress = loadProgress();

        if (!progress[category]) {
            progress[category] = {};
        }

        if (!progress[category][exercise]) {
            progress[category][exercise] = {
                attempted: true,
                completed: false
            };
        } else {
            progress[category][exercise].attempted = true;

            // Explicitly preserve completed state
            if (progress[category][exercise].completed !== true) {
                progress[category][exercise].completed = false;
            }
        }

        saveProgress(progress);
    }

    function markExerciseCompleted(category, exercise) {
        const progress = loadProgress();

        if (!progress[category]) {
            progress[category] = {};
        }

        if (!progress[category][exercise]) {
            progress[category][exercise] = {
                attempted: true,
                completed: true
            };
        } else {
            progress[category][exercise].attempted = true;
            progress[category][exercise].completed = true; // Never revert
        }

        saveProgress(progress);
    }

    function updateExerciseVisualState() {
        const progress = loadProgress();

        document.querySelectorAll(".exercise-card").forEach(card => {
            const url = card.getAttribute("href");
            if (!url) return;

            const match = url.match(/exercises\/([^\/]+)\/([^\/]+)/);
            if (!match) return;

            const category = match[1];
            const exercise = match[2];

            const state = progress[category]?.[exercise];

            let indicator = card.querySelector(".exercise-status");

            if (!indicator) {
                indicator = document.createElement("span");
                indicator.className = "exercise-status";
                card.prepend(indicator);
            }

            if (!state) {
                indicator.className = "exercise-status not-attempted";
            } else if (state.completed) {
                indicator.className = "exercise-status completed";
            } else if (state.attempted) {
                indicator.className = "exercise-status attempted";
            }
        });
    }

    function updateCategoryProgress() {
        const progress = loadProgress();

        document.querySelectorAll(".category-card").forEach(card => {
            const url = card.getAttribute("href");
            if (!url) return;

            const match = url.match(/exercises\/([^\/]+)/);
            if (!match) return;

            const category = match[1];

            const totalExercises = parseInt(card.dataset.count || "0");
            const completed = progress[category]
                ? Object.values(progress[category]).filter(e => e.completed).length
                : 0;

            const progressElement = card.querySelector(".progress-placeholder");

            if (progressElement) {
                progressElement.textContent = `${completed}/${totalExercises} completados`;
            }
        });
    }

    /* =========================
       HTMX HOOKS
    ========================== */

    document.addEventListener("DOMContentLoaded", function () {
        initializeApplication();

        document.addEventListener("click", function () {
            const dropdown = document.querySelector(".dropdown");
            if (dropdown) dropdown.classList.remove("open");
        });
    });

    document.body.addEventListener("htmx:historyRestore", function () {
        initializeApplication();
    });

    document.body.addEventListener("htmx:afterSwap", function (event) {
        if (event.target.id === "main-content") {
            initializeCodeEditor();
        }

        if (event.target.id === "result") {
            const resultElement = event.target;
            const statusContainer = resultElement.querySelector("#execution-status");

            if (!statusContainer) return;

            const categoryMatch = window.location.pathname.match(/exercises\/([^\/]+)\/([^\/]+)/);
            if (!categoryMatch) return;

            const category = categoryMatch[1];
            const exercise = categoryMatch[2];

            const status = statusContainer.dataset.status;

            // Always mark as attempted
            markExerciseAttempted(category, exercise);

            // Only mark as completed if pass
            if (status === "pass") {
                markExerciseCompleted(category, exercise);
            }

            updateExerciseVisualState();
            updateCategoryProgress();
        }
    });

    document.body.addEventListener("htmx:configRequest", function (event) {
        const textarea = document.getElementById("code-editor");

        if (!textarea || !textarea._editorInstance) return;

        const editor = textarea._editorInstance;
        const currentCode = editor.getValue();

        event.detail.parameters["code"] = currentCode;
    });

})();
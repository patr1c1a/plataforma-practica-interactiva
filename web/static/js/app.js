(function () {

    let activeCodeEditor = null;

    function initializeApplication() {
        initializeTheme();
        initializeDropdowns();
        initializeCodeEditor();
        initializeProgressPanel();
        initializeSidebar();
        updateProgressUI();
    }

    function updateProgressUI() {
        updateExerciseVisualState();
        updateCategoryProgress();
        updateSidebarProgress();
        updateSidebarCategoryProgress();
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

    function initializeDropdowns() {
        const dropdowns = document.querySelectorAll(".dropdown");

        dropdowns.forEach(dropdown => {
            const toggle = dropdown.querySelector(".dropdown-toggle");
            if (!toggle) return;

            toggle.addEventListener("click", function (event) {
                event.stopPropagation();

                dropdowns.forEach(d => {
                    if (d !== dropdown) {
                        d.classList.remove("open");
                    }
                });

                dropdown.classList.toggle("open");
            });
        });

        document.addEventListener("click", function () {
            dropdowns.forEach(d => d.classList.remove("open"));
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

            const progressContainer = card.querySelector(".category-progress-bar");
            const progressText = card.querySelector(".category-progress-text");

            if (!progressContainer || !progressText) return;

            const percentage = totalExercises > 0
                ? Math.round((completed / totalExercises) * 100)
                : 0;

            progressContainer.style.width = `${percentage}%`;
            applyProgressBarColor(progressContainer, percentage);
            progressText.textContent = `${completed}/${totalExercises} completados`;
        });
    }

    function applyProgressBarColor(barElement, percentage) {
        if (!barElement) return;

        barElement.classList.remove("progress-zero", "progress-partial", "progress-complete");

        if (percentage <= 0) {
            barElement.classList.add("progress-zero");
            return;
        }

        if (percentage >= 100) {
            barElement.classList.add("progress-complete");
            return;
        }

        barElement.classList.add("progress-partial");
    }

    function initializeProgressPanel() {
        const panel = document.getElementById("progress-panel");
        const button = document.getElementById("progress-button");

        if (!panel || !button) return;

        button.addEventListener("click", function (event) {
            event.stopPropagation();
            panel.classList.toggle("hidden");
        });

        document.addEventListener("click", function () {
            panel.classList.add("hidden");
        });

        initializeExport();
        initializeImport();
        initializeReset();
    }

    function initializeExport() {
        const exportButton = document.getElementById("export-progress");
        if (!exportButton) return;

        exportButton.addEventListener("click", function () {
            const progress = loadProgress();

            const exportData = {
                version: 1,
                exportedAt: new Date().toISOString(),
                progress: progress
            };

            const blob = new Blob(
                [JSON.stringify(exportData, null, 2)],
                { type: "application/json" }
            );

            const url = URL.createObjectURL(blob);

            const a = document.createElement("a");
            a.href = url;
            a.download = "progreso-plataforma.json";
            a.click();

            URL.revokeObjectURL(url);
        });
    }

    function initializeImport() {
        const input = document.getElementById("import-progress");
        if (!input) return;

        input.addEventListener("change", function (event) {
            const file = event.target.files[0];
            if (!file) return;

            const reader = new FileReader();

            reader.onload = function (e) {
                try {
                    const parsed = JSON.parse(e.target.result);

                    if (!parsed.version || !parsed.progress) {
                        return;
                    }

                    saveProgress(parsed.progress);
                    updateProgressUI();
                } catch {
                    return;
                }
            };

            reader.readAsText(file);
        });
    }

    function initializeReset() {
        const resetButton = document.getElementById("reset-progress");
        if (!resetButton) return;

        resetButton.addEventListener("click", function () {
            const confirmed = confirm("¿Estás seguro de que querés borrar todo el progreso?");
            if (!confirmed) return;

            localStorage.removeItem(PROGRESS_STORAGE_KEY);
            updateProgressUI();
        });
    }

    /* =========================
       SIDEBAR
    ========================== */

    function initializeSidebar() {
        const categories = document.querySelectorAll(".sidebar-category");

        categories.forEach(category => {
            const toggle = category.querySelector(".sidebar-category-toggle");

            toggle.addEventListener("click", function () {
                category.classList.toggle("open");
            });
        });
    }

    function updateSidebarProgress() {
        const progress = loadProgress();

        document.querySelectorAll(".sidebar-exercise-link").forEach(link => {
            const category = link.dataset.category;
            const exercise = link.dataset.exercise;

            const state = progress[category]?.[exercise];
            const indicator = link.querySelector(".sidebar-status");

            if (!indicator) return;

            if (!state) {
                indicator.className = "sidebar-status not-attempted";
            } else if (state.completed) {
                indicator.className = "sidebar-status completed";
            } else if (state.attempted) {
                indicator.className = "sidebar-status attempted";
            }
        });
    }

    function updateSidebarCategoryProgress() {
        const progress = loadProgress();

        document.querySelectorAll(".sidebar-category").forEach(categoryBlock => {
            const category = categoryBlock.dataset.category;
            const total = parseInt(categoryBlock.dataset.count || "0");

            const completed = progress[category]
                ? Object.values(progress[category]).filter(e => e.completed).length
                : 0;

            const percentage = total > 0
                ? Math.round((completed / total) * 100)
                : 0;

            const bar = categoryBlock.querySelector(".sidebar-category-progress-bar");
            const text = categoryBlock.querySelector(".sidebar-category-text");

            if (!bar || !text) return;

            bar.style.width = `${percentage}%`;
            applyProgressBarColor(bar, percentage);
            text.textContent = `${completed}/${total}`;
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

            updateProgressUI();
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

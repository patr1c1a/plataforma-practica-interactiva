(function () {

    let activeCodeEditor = null;
    let hasDropdownDocumentClickListener = false;
    let hasProgressPanelDocumentClickListener = false;

    function initializeApplication() {
        migrateExerciseCodeStorageToLocal();
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

        if (toggleButton.dataset.initialized === "true") return;
        toggleButton.dataset.initialized = "true";

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
            toggleButton.textContent = theme === "dark" ? "☀️" : "🌙";
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
        const closeAllDropdowns = function () {
            document.querySelectorAll(".dropdown").forEach(dropdown => {
                dropdown.classList.remove("open");
            });
        };

        const dropdowns = document.querySelectorAll(".dropdown");

        dropdowns.forEach(dropdown => {
            const toggle = dropdown.querySelector(".dropdown-toggle");
            if (!toggle) return;
            if (toggle.dataset.initialized === "true") return;
            toggle.dataset.initialized = "true";

            toggle.addEventListener("click", function (event) {
                event.stopPropagation();

                document.querySelectorAll(".dropdown").forEach(d => {
                    if (d !== dropdown) {
                        d.classList.remove("open");
                    }
                });

                dropdown.classList.toggle("open");
            });
        });

        if (!hasDropdownDocumentClickListener) {
            document.addEventListener("click", function () {
                closeAllDropdowns();
            });
            hasDropdownDocumentClickListener = true;
        }
    }

    /* =========================
       CODE EDITOR
    ========================== */

    function initializeCodeEditor() {
        if (typeof CodeMirror === "undefined") return;

        const textarea = document.getElementById("code-editor");
        if (!textarea) return;

        if (textarea._initialCode === undefined) {
            textarea._initialCode = textarea.value;
        }

        // If CodeMirror was already used, do not initialize again
        if (textarea._editorInstance) {
            activeCodeEditor = textarea._editorInstance;
            initializeExerciseResetButton();
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
        const savedCode = getStoredExerciseCode(storageKey);

        if (savedCode !== null) {
            editor.setValue(savedCode);
        }

        editor.on("change", function (cm) {
            setStoredExerciseCode(storageKey, cm.getValue());
        });

        activeCodeEditor = editor;

        initializeExerciseResetButton();
    }

    /* =========================
        PROGRESS
    ========================= */

    const PROGRESS_STORAGE_KEY = "platform-progress-v1";
    const EXERCISE_STORAGE_PREFIX = "exercise-";

    function getStoredExerciseCode(storageKey) {
        const persistentCode = localStorage.getItem(storageKey);
        if (persistentCode !== null) return persistentCode;

        const sessionCode = sessionStorage.getItem(storageKey);
        if (sessionCode !== null) {
            localStorage.setItem(storageKey, sessionCode);
            sessionStorage.removeItem(storageKey);
            return sessionCode;
        }

        return null;
    }

    function setStoredExerciseCode(storageKey, code) {
        localStorage.setItem(storageKey, code);
    }

    function clearStoredExerciseCodeByKey(storageKey) {
        localStorage.removeItem(storageKey);
        sessionStorage.removeItem(storageKey);
    }

    function migrateExerciseCodeStorageToLocal() {
        const keysToMigrate = [];

        for (let i = 0; i < sessionStorage.length; i += 1) {
            const key = sessionStorage.key(i);
            if (!key) continue;
            if (!key.startsWith(EXERCISE_STORAGE_PREFIX)) continue;
            keysToMigrate.push(key);
        }

        keysToMigrate.forEach(key => {
            if (localStorage.getItem(key) === null) {
                const code = sessionStorage.getItem(key);
                if (code !== null) {
                    localStorage.setItem(key, code);
                }
            }
            sessionStorage.removeItem(key);
        });
    }

    function loadProgress() {
        const raw = localStorage.getItem(PROGRESS_STORAGE_KEY);
        return raw ? JSON.parse(raw) : {};
    }

    function saveProgress(progressData) {
        localStorage.setItem(PROGRESS_STORAGE_KEY, JSON.stringify(progressData));
    }

    function buildExerciseStorageKey(category, exercise) {
        return `${EXERCISE_STORAGE_PREFIX}${category}-${exercise}`;
    }

    function collectExerciseCodeForExport(progressData) {
        const codeByExercise = {};

        Object.entries(progressData).forEach(([category, exercises]) => {
            Object.entries(exercises).forEach(([exercise, state]) => {
                if (!state?.attempted && !state?.completed) return;

                const storageKey = buildExerciseStorageKey(category, exercise);
                const code = getStoredExerciseCode(storageKey);

                if (!codeByExercise[category]) {
                    codeByExercise[category] = {};
                }

                // Export code for attempted/completed exercises, even if currently empty.
                codeByExercise[category][exercise] = code ?? "";
            });
        });

        return codeByExercise;
    }

    function restoreImportedExerciseCode(codeByExercise) {
        if (!codeByExercise || typeof codeByExercise !== "object") return;

        Object.entries(codeByExercise).forEach(([category, exercises]) => {
            Object.entries(exercises || {}).forEach(([exercise, code]) => {
                if (typeof code !== "string") return;

                const storageKey = buildExerciseStorageKey(category, exercise);
                setStoredExerciseCode(storageKey, code);
            });
        });
    }

    function clearStoredExerciseCode() {
        const keysToRemove = [];

        for (let i = 0; i < localStorage.length; i += 1) {
            const key = localStorage.key(i);
            if (!key) continue;

            if (key.startsWith(EXERCISE_STORAGE_PREFIX)) {
                keysToRemove.push(key);
            }
        }

        keysToRemove.forEach(key => clearStoredExerciseCodeByKey(key));
    }

    function clearExerciseProgress(category, exercise) {
        const progress = loadProgress();

        if (!progress[category] || !progress[category][exercise]) return;

        delete progress[category][exercise];

        if (Object.keys(progress[category]).length === 0) {
            delete progress[category];
        }

        saveProgress(progress);
    }

    function getCurrentExerciseFromPath() {
        const match = window.location.pathname.match(/exercises\/([^\/]+)\/([^\/]+)/);
        if (!match) return null;

        return {
            category: match[1],
            exercise: match[2]
        };
    }

    function initializeExerciseResetButton() {
        const resetExerciseButton = document.getElementById("reset-exercise");
        if (!resetExerciseButton || resetExerciseButton.dataset.initialized === "true") return;

        resetExerciseButton.dataset.initialized = "true";
        resetExerciseButton.addEventListener("click", function () {
            const textarea = document.getElementById("code-editor");
            if (!textarea || !textarea._editorInstance) return;

            const originalCode = textarea._initialCode ?? "";
            const storageKey = textarea.dataset.storageKey;

            textarea._editorInstance.setValue(originalCode);
            setStoredExerciseCode(storageKey, originalCode);

            const exerciseInfo = getCurrentExerciseFromPath();
            if (exerciseInfo) {
                clearExerciseProgress(exerciseInfo.category, exerciseInfo.exercise);
            }

            const resultContainer = document.getElementById("result");
            if (resultContainer) {
                resultContainer.innerHTML = "";
            }

            updateProgressUI();
        });
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

        if (button.dataset.initialized !== "true") {
            button.dataset.initialized = "true";
            button.addEventListener("click", function (event) {
                event.stopPropagation();
                panel.classList.toggle("hidden");
            });
        }

        if (!hasProgressPanelDocumentClickListener) {
            document.addEventListener("click", function () {
                const progressPanel = document.getElementById("progress-panel");
                if (progressPanel) {
                    progressPanel.classList.add("hidden");
                }
            });
            hasProgressPanelDocumentClickListener = true;
        }

        initializeExport();
        initializeImport();
        initializeReset();
    }

    function initializeExport() {
        const exportButton = document.getElementById("export-progress");
        if (!exportButton) return;
        if (exportButton.dataset.initialized === "true") return;
        exportButton.dataset.initialized = "true";

        exportButton.addEventListener("click", function () {
            const progress = loadProgress();
            const code = collectExerciseCodeForExport(progress);

            const exportData = {
                version: 2,
                exportedAt: new Date().toISOString(),
                progress: progress,
                code: code
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
        if (input.dataset.initialized === "true") return;
        input.dataset.initialized = "true";

        input.addEventListener("change", function (event) {
            const file = event.target.files[0];
            if (!file) return;

            const reader = new FileReader();

            reader.onload = function (e) {
                try {
                    const parsed = JSON.parse(e.target.result);
                    const progressData = parsed?.progress ?? parsed?.progreso ?? parsed;
                    const codeData = parsed?.code ?? parsed?.codigo ?? {};

                    if (
                        !progressData ||
                        typeof progressData !== "object" ||
                        Array.isArray(progressData)
                    ) {
                        alert("El archivo no contiene progreso vÃ¡lido.");
                        return;
                    }

                    saveProgress(progressData);
                    clearStoredExerciseCode();
                    restoreImportedExerciseCode(codeData);
                    refreshCurrentEditorFromStorage();
                    updateProgressUI();
                } catch (error) {
                    console.error("Error al importar progreso:", error);
                    alert("No se pudo importar el archivo seleccionado.");
                    return;
                } finally {
                    // Allow importing the same file again without changing file name.
                    input.value = "";
                }
            };

            reader.readAsText(file);
        });
    }

    function refreshCurrentEditorFromStorage() {
        const textarea = document.getElementById("code-editor");
        if (!textarea || !textarea._editorInstance) return;

        const storageKey = textarea.dataset.storageKey;
        if (!storageKey) return;

        const restoredCode = getStoredExerciseCode(storageKey);
        if (restoredCode === null) return;

        textarea._editorInstance.setValue(restoredCode);
    }

    function persistCurrentEditorCode() {
        const textarea = document.getElementById("code-editor");
        if (!textarea || !textarea._editorInstance) return;

        const storageKey = textarea.dataset.storageKey;
        if (!storageKey) return;

        setStoredExerciseCode(storageKey, textarea._editorInstance.getValue());
    }

    function initializeReset() {
        const resetButton = document.getElementById("reset-progress");
        if (!resetButton) return;
        if (resetButton.dataset.initialized === "true") return;
        resetButton.dataset.initialized = "true";

        resetButton.addEventListener("click", function () {
            const confirmed = confirm("Esto borra todo el progreso. ¿Deseas continuar?");
            if (!confirmed) return;

            localStorage.removeItem(PROGRESS_STORAGE_KEY);
            clearStoredExerciseCode();

            const textarea = document.getElementById("code-editor");
            if (textarea && textarea._editorInstance) {
                const originalCode = textarea._initialCode ?? "";
                const storageKey = textarea.dataset.storageKey;

                textarea._editorInstance.setValue(originalCode);
                if (storageKey) {
                    setStoredExerciseCode(storageKey, originalCode);
                }
            }

            const resultContainer = document.getElementById("result");
            if (resultContainer) {
                resultContainer.innerHTML = "";
            }

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
            if (!toggle) return;
            if (toggle.dataset.initialized === "true") return;
            toggle.dataset.initialized = "true";

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
        if ("scrollRestoration" in history) {
            history.scrollRestoration = "manual";
        }

        initializeApplication();
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

    document.body.addEventListener("htmx:beforeRequest", function (event) {
        const requestSource = event.detail.elt;
        if (!requestSource) return;

        if (
            requestSource.tagName !== "FORM" ||
            requestSource.getAttribute("hx-target") !== "#result"
        ) {
            return;
        }

        const resultContainer = document.getElementById("result");
        if (resultContainer) {
            resultContainer.innerHTML = "";
        }
    });

    document.body.addEventListener("htmx:configRequest", function (event) {
        const textarea = document.getElementById("code-editor");

        if (!textarea || !textarea._editorInstance) return;

        const editor = textarea._editorInstance;
        const currentCode = editor.getValue();
        const storageKey = textarea.dataset.storageKey;

        if (storageKey) {
            setStoredExerciseCode(storageKey, currentCode);
        }

        event.detail.parameters["code"] = currentCode;
    });

    window.addEventListener("beforeunload", function () {
        persistCurrentEditorCode();
    });

})();

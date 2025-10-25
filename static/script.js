document.addEventListener("DOMContentLoaded", function () {
  // Auto-hide alerts after 10 seconds
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach((alert) => {
    setTimeout(() => {
      alert.classList.add("fade-out");
      setTimeout(() => {
        alert.remove();
      }, 300);
    }, 10000);
  });

  // Drag and drop functionality
  const uploadZone = document.getElementById("uploadZone");
  const fileInput = document.getElementById("fileInput");
  const uploadLabel = document.getElementById("uploadLabel");
  const uploadForm = document.getElementById("uploadForm");

  if (uploadZone && fileInput) {
    // File input change handler
    fileInput.addEventListener("change", function () {
      const fileCount = this.files.length;
      if (fileCount > 0) {
        uploadLabel.textContent = `${fileCount} file(s) selected`;
        uploadLabel.style.background = "var(--success)";
      } else {
        uploadLabel.textContent = "📁 Choose Files";
        uploadLabel.style.background = "var(--primary)";
      }
    });

    // Drag and drop events
    ["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
      uploadZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
      e.preventDefault();
      e.stopPropagation();
    }

    ["dragenter", "dragover"].forEach((eventName) => {
      uploadZone.addEventListener(eventName, highlight, false);
    });

    ["dragleave", "drop"].forEach((eventName) => {
      uploadZone.addEventListener(eventName, unhighlight, false);
    });

    function highlight() {
      uploadZone.classList.add("dragover");
      uploadZone.style.borderColor = "var(--primary)";
      uploadZone.style.background = "rgba(67, 97, 238, 0.1)";
    }

    function unhighlight() {
      uploadZone.classList.remove("dragover");
      uploadZone.style.borderColor = "";
      uploadZone.style.background = "";
    }

    // Handle file drop
    uploadZone.addEventListener("drop", handleDrop, false);

    function handleDrop(e) {
      const dt = e.dataTransfer;
      const files = dt.files;
      fileInput.files = files;

      // Update label
      const fileCount = files.length;
      if (fileCount > 0) {
        uploadLabel.textContent = `${fileCount} file(s) selected`;
        uploadLabel.style.background = "var(--success)";

        // Auto-submit form after a brief delay
        setTimeout(() => {
          uploadForm.submit();
        }, 100);
      }
    }
  }

  // Enhanced file preview for images
  const previewImages = document.querySelectorAll(".preview-image");
  previewImages.forEach((img) => {
    img.addEventListener("error", function () {
      this.style.display = "none";
      const placeholder = this.nextElementSibling;
      if (placeholder) {
        placeholder.style.display = "flex";
      }
    });
  });

  // Keyboard shortcuts
  document.addEventListener("keydown", function (e) {
    // Ctrl/Cmd + N for new folder
    if ((e.ctrlKey || e.metaKey) && e.key === "n") {
      e.preventDefault();
      document.getElementById("createFolderBtn").click();
    }

    // Escape key to close modal
    if (e.key === "Escape") {
    }
  });
});

// Global functions for template
function navigateToFolder(path) {
  window.location.href = `/files/${path}`;
}

function confirmDelete(type, name) {
  const message =
    type === "folder"
      ? `Are you sure you want to delete the folder "${name}" and all its contents? This action cannot be undone.`
      : `Are you sure you want to delete the file "${name}"? This action cannot be undone.`;
  return confirm(message);
}

function closeUploadModal() {
  document.getElementById("uploadModal").style.display = "none";
  // Reset form
  const form = document.querySelector("#uploadForm");
  if (form) {
    form.reset();
  }
}

function validateFolderForm() {
  const input = document.getElementById("newFolderName");
  const saveBtn = document.getElementById("folderSaveBtn");

  if (input && input.value.trim()) {
    saveBtn.disabled = false;
    return true;
  } else {
    saveBtn.disabled = true;
    return false;
  }
}

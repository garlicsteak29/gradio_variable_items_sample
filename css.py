def get_app_css():
    return """
.delete_lora_button {
    height: -webkit-fill-available;
    max-width: fit-content;
    min-width: fit-content;
}
.use_lora {
    background: transparent;
    padding: 0;
}
.lora_root_container > * {
    padding: 8px;
    gap: 8px;
}
.lora_files > * {
    margin: 8px 0 0 0;
    gap: 8px;
}
.lora_row {
    padding: 5px;
    gap: 5px;
    background: #909090;
}

.info_button {
    max-width: fit-content;
}
textarea {
    scrollbar-width: thin;
}
"""
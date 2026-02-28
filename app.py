import json
import gradio as gr

from css import get_app_css

with gr.Blocks(css=get_app_css()) as demo:
    lora_files = gr.State([])
    with gr.Row():
        lora_info_getter = gr.Button(
            "get LORA info",
            elem_classes="info_button",
        )
        lora_info_display = gr.Textbox(
            lines=5,
            max_lines=5,
            interactive=False,
        )
    def get_loras_info(loras):
        return json.dumps(obj=loras, ensure_ascii=False, indent=2)
    with gr.Group(elem_classes="lora_root_container"):
        def get_lora_toggle_label(num=None):
            if not isinstance(num, int):
                num = 0
            return "use LORA" + f" ({num})"
        def update_lora_toggle_label(num=None):
            return gr.update(label=get_lora_toggle_label(num))
        use_lora = gr.Checkbox(
            label=get_lora_toggle_label(),
            value=True,
            elem_classes="use_lora"
        )
        lora_num = gr.State(0)
        lora_num.change(
            fn=update_lora_toggle_label,
            inputs=lora_num,
            outputs=use_lora,
        )
        with gr.Group() as group:
            @gr.render(inputs=lora_files)
            def render_rows(loras):
                add_button = gr.Button(
                    value="+",
                    variant="primary",
                )
                def push(states, lora_num):
                    # gr.Stateの変更検知のため足し算によるコピーを返す
                    return states + [(None, .3)], lora_num + 1
                add_button.click(
                    fn=push,
                    inputs=[lora_files, lora_num],
                    outputs=[lora_files, lora_num],
                )
                with gr.Group(elem_classes="lora_files"):
                    for i, (path, scale) in enumerate(loras):
                        with gr.Row(elem_classes="lora_row"):
                            remove_button = gr.Button(
                                value="✕",
                                elem_classes="delete_lora_button"
                            )
                            with gr.Column():
                                file = gr.File(
                                    label="LoRAファイル (.safetensors, .pt, .bin)",
                                    file_types=[".safetensors", ".pt", ".bin"],
                                    value=path,
                                    height=44,
                                    show_label=False,
                                )
                                slider = gr.Slider(
                                    minimum=0,
                                    maximum=2,
                                    value=scale,
                                    step=.1,
                                )
                        def change(loras, i, path, scale):
                            loras[i] = (path, scale)
                            # return loras
                        file.change(
                            fn=change,
                            inputs=[
                                lora_files,
                                gr.State(i),
                                file,
                                slider,
                            ],
                            # outputs=lora_files,
                        )
                        slider.change(
                            fn=change,
                            inputs=[
                                lora_files,
                                gr.State(i),
                                file,
                                slider,
                            ],
                            # outputs=lora_files,
                        )
                        def pop(states, i, lora_num):
                            # copy()はgr.Stateの変更検知用
                            states = states.copy()
                            states.pop(i)
                            return states, lora_num - 1
                        remove_button.click(
                            fn=pop,
                            inputs=[lora_files, gr.State(i), lora_num],
                            outputs=[lora_files, lora_num],
                        )
    lora_info_getter.click(
        fn=get_loras_info,
        inputs=lora_files,
        outputs=lora_info_display,
    )
    use_lora.change(
        fn=lambda x: gr.update(visible=x),
        inputs=use_lora,
        outputs=[
            group,
        ],
    )
demo.launch()
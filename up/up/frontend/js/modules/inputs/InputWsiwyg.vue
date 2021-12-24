<template>
    <div class="wysiwyg">
        <div data-role="editor-toolbar" data-target="#editor" v-if="editor">
            <!-- text size -->
            <div class="btn-group">
                <button type="button" class="btn dropdown-toggle" data-bs-toggle="dropdown" title="Font size"
                        aria-expanded="false">
                    <i class="fas fa-text-height"></i>
                </button>
                <ul class="dropdown-menu">
                    <li :class="{ '-color-moderategray': editor.isActive('heading', {level: 1}) }"
                        @click="editor.chain().focus().toggleHeading({level: 1}).run()">
                        <a class="dropdown-item" href="#">
                            <h1>Heading 1</h1>
                        </a>
                    </li>
                    <li :class="{ '-color-moderategray': editor.isActive('heading', {level: 2}) }"
                        @click="editor.chain().focus().toggleHeading({level: 2}).run()">
                        <a class="dropdown-item" href="#">
                            <h2>Heading 2</h2>
                        </a>
                    </li>
                    <li :class="{ '-color-moderategray': editor.isActive('heading', {level: 3}) }"
                        @click="editor.chain().focus().toggleHeading({level: 3}).run()">
                        <a class="dropdown-item" href="#">
                            <h3>Heading 3</h3>
                        </a>
                    </li>
                    <li :class="{ '-color-moderategray': editor.isActive('paragraph') }"
                        @click="editor.chain().focus().setParagraph().run()">
                        <a class="dropdown-item" href="#">
                            <p>Normal</p>
                        </a>
                    </li>
                </ul>

                <!-- text format -->
                <button type="button" class="btn" title="Bold (Ctrl/Cmd+B)"
                        @click="editor.chain().focus().toggleBold().run()"
                        :class="{ '-color-moderategray': editor.isActive('bold') }">
                    <i class="fas fa-bold"></i>
                </button>
                <button type="button" class="btn" title="Italic (Ctrl/Cmd+I)"
                        @click="editor.chain().focus().toggleItalic().run()"
                        :class="{ '-color-moderategray': editor.isActive('italic') }">
                    <i class="fas fa-italic"></i>
                </button>
                <button type="button" class="btn" title="Underline (Ctrl/Cmd+Shift+X)"
                        @click="editor.chain().focus().toggleStrike().run()"
                        :class="{ '-color-moderategray': editor.isActive('strike') }">
                    <i class="fas fa-strikethrough"></i>
                </button>
                <button type="button" class="btn" title="Underline (Ctrl/Cmd+U)"
                        @click="editor.chain().focus().toggleUnderline().run()"
                        :class="{ '-color-moderategray': editor.isActive('underline') }">
                    <i class="fas fa-underline"></i>
                </button>

                <!-- Lists and indent -->
                <button type="button" class="btn" title="Bullet list (Ctrl/Cmd+Shift+8)"
                        @click="editor.chain().focus().toggleBulletList().run()"
                        :class="{ '-color-moderategray': editor.isActive('bulletList') }">
                    <i class="fas fa-list-ul"></i>
                </button>
                <button type="button" class="btn" title="Numbered list (Ctrl/Cmd+Shift+7)"
                        @click="editor.chain().focus().toggleOrderedList().run()"
                        :class="{ '-color-moderategray': editor.isActive('orderedList') }">
                    <i class="fas fa-list-ol"></i>
                </button>

                <!-- Alignment -->
                <button type="button" class="btn" title="Align Left (Ctrl/Cmd+L)"
                        @click="editor.chain().focus().setTextAlign('left').run()"
                        :class="{ '-color-moderategray': editor.isActive({ textAlign: 'left' }) }">
                    <i class="fas fa-align-left"></i>
                </button>
                <button type="button" class="btn" title="Center (Ctrl/Cmd+E)"
                        @click="editor.chain().focus().setTextAlign('center').run()"
                        :class="{ '-color-moderategray': editor.isActive({ textAlign: 'center' }) }">
                    <i class="fas fa-align-center"></i>
                </button>
                <button type="button" class="btn" title="Align Right (Ctrl/Cmd+R)"
                        @click="editor.chain().focus().setTextAlign('right').run()"
                        :class="{ '-color-moderategray': editor.isActive({ textAlign: 'right' }) }">
                    <i class="fas fa-align-right"></i>
                </button>
                <button type="button" class="btn" title="Justify (Ctrl/Cmd+J)"
                        @click="editor.chain().focus().setTextAlign('justify').run()"
                        :class="{ '-color-moderategray': editor.isActive({ textAlign: 'justify' }) }">
                    <i class="fas fa-align-justify"></i>
                </button>
            </div>
            <div class="btn-group">

                <button type="button" class="btn" title="Block quote"
                        @click="editor.chain().focus().toggleBlockquote().run()"
                        :class="{ '-color-moderategray': editor.isActive('blockquote') }">
                    <i class="fas fa-quote-left"></i>
                </button>
                <button type="button" class="btn" title="Horizontal rule"
                        @click="editor.chain().focus().setHorizontalRule().run()">---
                </button>

                <!-- Hyperlink -->
                <button type="button" class="btn dropdown-toggle" data-bs-toggle="dropdown"
                        data-original-title="Hyperlink" aria-expanded="false" @click="setUrl">
                    <i class="fas fa-link"></i>
                </button>
                <div class="dropdown-menu input-append url-form">
                    <div class="input-group">
                        <input type="text" class="form-control" placeholder="URL" v-model="url"
                               @mousedown="saveTextSelection" @focus="setTextSelection">
                        <button class="btn btn-outline-secondary" type="button" @click="saveLink">Add</button>
                    </div>
                </div>
                <button type="button" class="btn" @click="editor.chain().focus().unsetLink().run()">
                    <i class="fas fa-unlink"></i>
                </button>

                <!-- Undo/redo -->
                <button type="button" class="btn" title="Undo (Ctrl/Cmd+Z)"
                        @click="editor.chain().focus().undo().run()">
                    <i class="fas fa-undo"></i>
                </button>
                <button type="button" class="btn" title="Redo (Ctrl/Cmd+Y)"
                        @click="editor.chain().focus().redo().run()">
                    <i class="fas fa-redo"></i>
                </button>
            </div>
        </div>

        <!-- The editor -->
        <editor-content :editor="editor" :id="elId"/>
    </div>
</template>
<script>
import {Editor, EditorContent} from '@tiptap/vue-3';
import Blockquote from '@tiptap/extension-blockquote';
import Bold from '@tiptap/extension-bold';
import BulletList from '@tiptap/extension-bullet-list';
import Document from '@tiptap/extension-document';
import Dropcursor from '@tiptap/extension-dropcursor';
import Heading from '@tiptap/extension-heading';
import Highlight from '@tiptap/extension-highlight';
import History from '@tiptap/extension-history';
import HorizontalRule from '@tiptap/extension-horizontal-rule';
import Italic from '@tiptap/extension-italic';
import Link from '@tiptap/extension-link';
import ListItem from '@tiptap/extension-list-item';
import OrderedList from '@tiptap/extension-ordered-list';
import Paragraph from '@tiptap/extension-paragraph';
import Placeholder from '@tiptap/extension-placeholder';
import Strike from '@tiptap/extension-strike';
import Text from '@tiptap/extension-text';
import TextAlign from '@tiptap/extension-text-align';
import Underline from '@tiptap/extension-underline';

export default {
    components: {
        EditorContent
    },

    props: {
        modelValue: {
            type: String,
            default: '',
        },
        placeholder: {
            type: String,
            default: 'Write something...'
        },
        elId: {
            type: String
        }
    },

    data() {
        return {
            editor: null,
            url: null,
            textSelection: null
        }
    },
    watch: {
        modelValue(value) {
            // HTML
            const isSame = this.editor.getHTML() === value

            // JSON
            // const isSame = this.editor.getJSON().toString() === value.toString()

            if (isSame) {
                return;
            }

            this.editor.commands.setContent(this.modelValue, false)
        },
    },
    methods: {
        saveLink() {
            this.setTextSelection();
            const fullUrl = (this.url.match(/^http(s)?:\/\//)) ? this.url : `https://${this.url}`;
            this.editor.chain().focus().setLink({href: fullUrl}).run();
            this.url = null;
        },
        setUrl() {
            const state = this.editor.state

            // get marks, if any from selected area
            const {from, to} = state.selection;
            let marks = [];
            state.doc.nodesBetween(from, to, (node) => {
                marks = [...marks, ...node.marks]
            });

            const mark = marks.find((markItem) => markItem.type.name === 'link');
            this.url = (mark) ? mark.attrs.href : null;
        },
        saveTextSelection() {
            this.editor.commands.extendMarkRange('link');
            const {from, to} = this.editor.state.selection;
            this.textSelection = {from, to};
        },
        setTextSelection() {
            this.editor.commands.setTextSelection(this.textSelection);
            this.editor.commands.toggleHighlight({color: '#e1e3e6'});
        }
    },
    mounted() {
        this.editor = new Editor({
            extensions: [
                Blockquote,
                Bold,
                BulletList,
                Document,
                Dropcursor,
                Heading.configure({levels: [1, 2, 3]}),
                Highlight.configure({multicolor: true}),
                History,
                HorizontalRule,
                Italic,
                Link,
                ListItem,
                OrderedList,
                Paragraph,
                Placeholder.configure({placeholder: this.placeholder}),
                Strike,
                Text,
                TextAlign.configure({
                    types: ['heading', 'paragraph'],
                }),
                Underline
            ],
            editorProps: {
                attributes: {
                    class: 'form-control'
                }
            },
            // autofocus: true,
            content: this.modelValue,
            onBlur: () => {
                // HTML
                this.$emit('update:modelValue', this.$sanitize(this.editor.getHTML()));

                // JSON
                // this.$emit('input', this.editor.getJSON())
            },
        });
    },

    beforeDestroy() {
        this.editor.destroy()
    },
}
</script>
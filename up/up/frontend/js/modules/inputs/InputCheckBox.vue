<template>
    <div class="form-check">
        <input class="form-check-input" type="checkbox"
               :checked="(isChecked) ? true : null"
               :id="elId" @click="$emit('click', $event.target.checked)"
               :disabled="(isDisabled) ? true : null"
        >
        <template v-if="isEditable">
            <textarea v-if="isEditableTextArea"
                rows="2" class="form-control"
                :placeholder="editablePlaceHolder" :value="label"
                @change="$emit('change', $event.target.value)"
            />
            <input v-else type="text" class="form-control"
               :placeholder="editablePlaceHolder" :value="label"
               @change="$emit('change', $event.target.value)"
            >
        </template>
        <label v-else class="form-check-label" :for="(isActiveLabel) ? elId : null">
            {{label}}
        </label>
    </div>
</template>

<script>
export default {
    name: "InputCheckBox",
    props: ['label', 'isChecked', 'elId', 'isActiveLabel', 'isEditable', 'isEditableTextArea', 'editablePlaceHolder', 'isDisabled'],
    emits: ['click', 'change']
}
</script>
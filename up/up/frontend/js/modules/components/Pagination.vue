<template>
    <div v-if="pageCount > 1" class="btn-group" role="group" style="max-width: 400px;">
        <button
            v-if="currentPageNumber > 1"
            type="button" class="btn btn-secondary"
            @click="changePage({pageInc: -1})"
        >
            <i class="fas fa-arrow-left"></i>
        </button>
        <button
            v-for="pageNumber in pages"
            type="button"
            class="btn"
            :class="(pageNumber === currentPageNumber) ? 'btn-info' : 'btn-secondary'"
            @click="changePage({pageNumber})"
        >
            {{pageNumber}}
        </button>
        <button
            v-if="currentPageNumber < pageCount"
            type="button"
            class="btn btn-secondary"
            @click="changePage({pageInc: 1})"
        >
            <i class="fas fa-arrow-right"></i>
        </button>
    </div>
</template>

<script>
export default {
    name: "Pagination",
    props: ['items', 'itemsPerPage'],
    data() {
        return {
            defaultItemsPerPage: 25,
            currentPageNumber: 1,
        }
    },
    computed: {
        pageCount() {
            if (!this.items) {
                return 0;
            }
            return this.items.length / (this.itemsPerPage || this.defaultItemsPerPage);
        },
        showPageCount() {
            return Math.min(this.pageCount, 5);
        },
        startPage() {
            return Math.max(this.currentPageNumber - 2, 1)
        },
        pages() {
            const pages = [];
            for (let i=0; i<this.showPageCount && i+this.startPage <= this.pageCount + 1; i++) {
                pages.push(i+this.startPage);
            }
            return pages;
        }
    },
    methods: {
        changePage({pageNumber, pageInc}) {
            if (pageNumber) {
                this.currentPageNumber = pageNumber;
            } else {
                this.currentPageNumber += pageInc;
            }
            this.$emit('pageChange', this.currentPageNumber);
        },
        reset() {
            this.currentPageNumber = 1;
            this.$emit('pageChange', this.currentPageNumber);
        }
    }
}
</script>
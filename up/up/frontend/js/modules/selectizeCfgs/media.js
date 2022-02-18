

class MediaSelectize {
    DELIMITER = '-'

    getCompositeId(mediaType, id) {
        return `${mediaType}${this.DELIMITER}${id}`;
    }

    getParsedCompositeId(val) {
        const [mediaType, id] = val.split(this.DELIMITER);
        return {type: mediaType, id};
    }
}

const mediaSelectize = new MediaSelectize();

export default mediaSelectize;
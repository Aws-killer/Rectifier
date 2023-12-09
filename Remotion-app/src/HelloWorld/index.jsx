import {AbsoluteFill} from 'remotion';
import VideoStream from './VideoStream';
import {TextStream} from './TextStream';

import AudioStream from './AudioStream';
import ImageStream from './ImageStream';

export const HelloWorld = () => {
	return (
		<AbsoluteFill style={{position: 'relative', backgroundColor: 'black'}}>
			<ImageStream />
			<TextStream />
			<VideoStream />
			<AudioStream />
		</AbsoluteFill>
	);
};

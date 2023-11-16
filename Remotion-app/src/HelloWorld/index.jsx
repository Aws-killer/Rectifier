import {AbsoluteFill} from 'remotion';
import VideoStream from './VideoStream';
import {TextStream} from './TextStream';
import AudioStream from './AudioStream';

export const HelloWorld = () => {
	return (
		<AbsoluteFill style={{position: 'relative', backgroundColor: 'black'}}>
			<TextStream />
			<VideoStream />
			<AudioStream />
		</AbsoluteFill>
	);
};

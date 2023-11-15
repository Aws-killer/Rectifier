import {Subtitle} from './Subtitle';
import {
	spring,
	AbsoluteFill,
	useCurrentFrame,
	useVideoConfig,
	Audio,
	staticFile,
	Video,
} from 'remotion';
import {preloadAudio, resolveRedirect} from '@remotion/preload';

export const HelloWorld = ({titleText, titleColor}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const scale = spring({
		fps,
		frame,
		config: {
			damping: 200,
			mass: 0.5,
			stiffness: 200,
			overshootClamping: false,
			restDisplacementThreshold: 0.01,
			restSpeedThreshold: 0.01,
		},
	});

	return (
		<AbsoluteFill style={{position: 'relative', backgroundColor: 'black'}}>
			<Audio
				volume={0.15}
				src={staticFile('background.mp3')}
				// src={'https://yakova-streamer.hf.space/download/20707'}
			/>

			{/* <Video
				src={
					'https://player.vimeo.com/external/514185553.hd.mp4?s=33cb766901019185385a757eab89a9fd0d50d0c0&profile_id=172&oauth2_token_id=57447761'
				}
			/> */}
			{/* <Audio src={'https://yakova-streamer.hf.space/download/20711'} /> */}
			{/* <img src={''} style={{transform: `scale(${scale})`}} /> */}

			<Subtitle />
		</AbsoluteFill>
	);
};

import {AbsoluteFill} from 'remotion';
import React, {useMemo} from 'react';
import {
	staticFile,
	useVideoConfig,
	Img,
	Easing,
	useCurrentFrame,
	interpolate,
} from 'remotion';
import imageSequences from './Assets/ImageSequences.json';
import {TransitionSeries} from '@remotion/transitions';

const ImageStream = React.memo(() => {
	const {fps} = useVideoConfig();

	const imageComponents = useMemo(() => {
		return imageSequences.map((entry, index) => (
			<TransitionSeries.Sequence
				key={index}
				durationInFrames={fps * (entry.end - entry.start)}
			>
				<Images key={index} entry={entry} />
			</TransitionSeries.Sequence>
		));
	}, [fps]);

	return (
		<AbsoluteFill
			style={{
				top: '50%',
				left: '50%',
				transform: 'translate(-50%, -50%)',
				color: 'white',
				position: 'absolute',
				width: '100%',
				height: '100%',
				zIndex: 0,
				objectFit: 'cover',
			}}
		>
			<TransitionSeries>{imageComponents}</TransitionSeries>
		</AbsoluteFill>
	);
});

const Images = React.memo(({entry}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();

	const duration = useMemo(() => fps * 2.5, [fps]);
	const ImgScale = useMemo(
		() =>
			interpolate(frame, [0, duration], [1, 1.2], {
				easing: Easing.bezier(0.65, 0, 0.35, 1),
				extrapolateRight: 'clamp',
				extrapolateLeft: 'clamp',
			}),
		[frame, duration]
	);

	return (
		<AbsoluteFill
			style={{
				backgroundColor: 'black',
			}}
		>
			<Img
				id="imagex"
				style={{
					transform: `translate(-50%, -50%) scale(${ImgScale})`,
					position: 'absolute',
					top: '50%',
					left: '50%',
					width: 1080,
					height: 1920,
					objectFit: 'cover',
				}}
				src={staticFile(entry.name)}
			/>
		</AbsoluteFill>
	);
});

export default ImageStream;

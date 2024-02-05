import {
	AbsoluteFill,
	Series,
	interpolate,
	spring,
	useCurrentFrame,
} from 'remotion';
import React from 'react';
import {staticFile, useVideoConfig, Img, Easing} from 'remotion';
import imageSequences from './Assets/ImageSequences.json';
import {TransitionSeries, linearTiming} from '@remotion/transitions';
import GsapAnimation from './Components/GsapAnimation';
import gsap from 'gsap';

export default function ImageStream() {
	const {fps} = useVideoConfig();

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
			<TransitionSeries>
				{imageSequences.map((entry, index) => {
					return (
						<>
							<TransitionSeries.Sequence
								key={entry.start}
								durationInFrames={fps * (entry.end - entry.start)}
							>
								<Images key={index} entry={entry} />;
							</TransitionSeries.Sequence>
						</>
					);
				})}
			</TransitionSeries>
		</AbsoluteFill>
	);
}

const Images = ({entry}) => {
	const gsapTimeline = () => {
		let tlContainer = gsap.timeline();
		tlContainer.fromTo(
			'#gaussianBlur',
			{
				attr: {stdDeviation: `250,0`},
			},
			{
				attr: {stdDeviation: `0,0`},

				duration: 1/2,
			},
			0
		);
		return tlContainer;
	};
	return (
		<>
		<GsapAnimation
			style={{
				BackgroundColor: 'black',
			}}
			className="bg-black"
			Timeline={gsapTimeline}
		>
			<Audio src={staticFile('sfx_1.mp3')} />
			<svg xmlns="http://www.w3.org/2000/svg" version="1.1" className="filters">
				<defs>
					<filter id="blur">
						<feGaussianBlur
							id="gaussianBlur"
							in="SourceGraphic"
						/>
					</filter>
				</defs>
			</svg>
			<Img
							id="imagex"
				style={{
					filter: `url(#blur)`,
					objectPosition: 'center',
					objectFit: 'cover',

					position: 'absolute',
					top: '50%', // Center vertically
					left: '50%', // Center horizontally
					transform: 'translate(-50%, -50%)',

					width: 1080,
					height: 1920,

				}}
				src={staticFile(entry.name)}
			/>
					</GsapAnimation>
		</>
	);
};

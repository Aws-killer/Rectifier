import React, {createElement} from 'react';
import {useVideoConfig} from 'remotion';
import {loadFont as loadMain} from '@remotion/google-fonts/Bungee';
import transcriptData from './Transcription.json';
const {fontFamily: fontFamily2} = loadMain();
import {TransitionSeries} from '@remotion/transitions';

const codeStyle = (index) => {
	return {
		color: 'white',
		position: 'absolute',
		backgroundColor: 'red',
		top: '50%',
		width: '100%',
		transform: 'translate(-50%, -50%)',
		left: '50%',
	};
};

const subtitle = {
	fontFamily: fontFamily2,
	fontSize: 120,
	textAlign: 'center',
	display: 'relative',
	bottom: 140,
	width: '100%',
};

export const Subtitle = () => {
	const {fps} = useVideoConfig();

	return (
		<div style={subtitle}>
			<TransitionSeries>
				{transcriptData.map((entry, index) => {
					return (
						<TransitionSeries.Sequence
							from={entry.start * fps}
							durationInFrames={fps * (entry.end - entry.start)}
						>
							<Letter index={index} color="#0b84f3">
								{entry.text}
							</Letter>
						</TransitionSeries.Sequence>
					);
				})}
			</TransitionSeries>
		</div>
	);
};

export function Letter({children, color, index}) {
	const x = codeStyle(index);
	return createElement(
		'div',
		{className: 'greeting', style: {...x, color: 'white'}},
		children
	);
}

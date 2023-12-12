import React, {createElement} from 'react';
import {useVideoConfig, AbsoluteFill, TransitionSeries} from 'remotion';
import * as Fonts from '@remotion/google-fonts';
import transcriptData from './Assets/TextSequences.json';
import {FONT_FAMILY} from './constants';
import {TransitionSeries} from '@remotion/transitions';

const codeStyle = (index) => {
	return {
		color: 'white',
		position: 'absolute',
		top: '50%',
		zIndex: 50,
		transform: 'translate(-50%, -50%)',
		left: '50%',
	};
};

const subtitle = {
	fontFamily: FONT_FAMILY,
	fontSize: 90,
	textAlign: 'center',
	display: 'absolute',
	bottom: 140,
	width: '100%',
};

Fonts.getAvailableFonts()
	.filter((font) => {
		return font.fontFamily === FONT_FAMILY;
	})[0]
	.load()
	.then((font) => font.loadFont());

export const TextStream = () => {
	const {fps} = useVideoConfig();

	return (
		<AbsoluteFill
			style={{
				backgroundColor: 'transparent',
				justifyContent: 'center',
				alignItems: 'center',
				position: 'relative',
				color: 'white',
				fontSize: 120,
				fontFamily: FONT_FAMILY,
				fontWeight: 'bolder',
				WebkitBackfaceVisibility: 'hidden',
			}}
		>
			<TransitionSeries>
				{transcriptData.map((entry, index) => {
					return (
						<TransitionSeries.Sequence
							style={subtitle}
							key={index}
							from={entry.start * fps}
							durationInFrames={fps * (entry.end - entry.start) + 1}
						>
							<Letter style={subtitle} index={index} color="#0b84f3">
								{entry.text}
							</Letter>
						</TransitionSeries.Sequence>
					);
				})}
			</TransitionSeries>
		</AbsoluteFill>
	);
};

export function Letter({children, color, index, style}) {
	return createElement('div', {style: style}, children);
}

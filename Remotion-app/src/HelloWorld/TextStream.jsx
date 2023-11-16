import React, {createElement} from 'react';
import {useVideoConfig} from 'remotion';
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
	fontSize: 120,
	textAlign: 'center',
	display: 'relative',
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
		<div style={{...temp, ...{}}}>
			<TransitionSeries>
				{transcriptData.map((entry, index) => {
					return (
						<>
							<TransitionSeries.Sequence
								from={entry.start * fps}
								durationInFrames={fps * (entry.end - entry.start)}
							>
								<Letter index={index} color="#0b84f3">
									{entry.text}
								</Letter>
							</TransitionSeries.Sequence>
						</>
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
